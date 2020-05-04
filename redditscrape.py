#!/usr/bin/python3.7
###webscrape.py###
#Reference: https://www.datacamp.com/community/tutorials/scraping-reddit-python-scrapy
#Reference: https://www.thepythoncode.com/article/using-proxies-using-requests-in-python
#Reference: https://www.sylvaindurand.org/use-tor-with-python/
import requests
from bs4 import BeautifulSoup
import time
import json
import os
from stem.control import Controller
from stem import Signal
import sys

class Scraper:
    def __init__(self,subreddit):
        self.data = {'data': []}
        self.subreddit = subreddit
        self.outputfile = "data/" + subreddit + ".json"
        self.proxies = {"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}
        self.headers = {'User-Agent': 'Mozilla/5.0'}
    

    @staticmethod
    def get_tor_session():
        """
        need to run Tor service on port 9050 (by default)
        """
        session = requests.Session()
        session.proxies = {"http":"socks5://localhost:9050", "https": "socks5://localhost:9050"}
        return session
    
    @staticmethod
    def renew_connection():
        """
        renews Tor service to get new proxy
        """
        with Controller.from_port(port=9051) as c:
            c.authenticate()
            c.signal(Signal.NEWNYM)

    def webscrape_subreddit(self,url):
        self.renew_connection()
        page = requests.get(url, headers=self.headers, proxies=self.proxies)

        soup = BeautifulSoup(page.text, 'html.parser')
        domain = 'self.'+ self.subreddit
        attrs = {'class': 'thing', 'data-domain': domain}
        data = {'data' : []}
        for post in soup.find_all('div', attrs=attrs):
            title = post.find('p', class_="title")
            if title.find('span', class_="linkflairlabel"):
                flair = title.find('span', class_="linkflairlabel").text
                title = title.text.replace(flair," ")
            else:
                title = title.text
            print(title)
            comments= post.find('a', class_='comments').text
            comments = post.find('a', class_='comments').text.split()[0]
            if comments == "comment":
                comments = 0
            likes = post.find("div", attrs={"class": "score likes"}).text
            if likes == "•":
                likes = 0
            post_link = post.attrs["data-permalink"]
            post_link = "https://old.reddit.com" + post_link
            post_content = self.webscrape_post(post_link)
            data['data'].append({
                'title': title,
                'likes': likes,
                'comments': comments,
                'content': post_content
            })
            time.sleep(2)
        return data

    def webscrape_post(self,url):
        page = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(page.text, 'html.parser')
        post = soup.find('div', class_='thing')
        post_content = ""
        post_content = post.find('div', class_='usertext-body') if post != None else None
        post_content = post_content.text if post_content != None else "" #in case post has no content
        return post_content

    def getNextPage(self,url):
        page = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(page.text, 'html.parser')
        next_button = soup.find("span", class_="next-button")
        if next_button == None:
            return None
        next_page_link = next_button.find("a").attrs['href']
        return next_page_link

    def webcrawl(self,no_pages):
        sub_url = "https://old.reddit.com/r/"+ self.subreddit
        extensions = ["", "/top/","/gilded/"]
        self.data['data'] = []
        for extension in extensions:
            current_url = sub_url + extension
            for page in range(no_pages+1):
                if current_url == None:
                    break
                page_data = self.webscrape_subreddit(current_url)
                self.data['data'].append(page_data['data'])
                current_url = self.getNextPage(current_url)
                print(current_url)
                time.sleep(2)
        self.write_to_file()

    def write_to_file(self):
        if os.path.exists(self.outputfile):
            os.remove(self.outputfile)
        with open(self.outputfile, 'a') as f:
            json.dump(self.data, f)


if __name__ == "__main__":
    """
    Inputs:
        [1]: subreddit
        [2]: no_pages
    """

    subreddit = sys.argv[1]
    no_pages = int(sys.argv[2])
    redditScrapper = Scraper(subreddit)
    redditScrapper.webcrawl(no_pages)
