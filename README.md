# Subreddit Wordclouds
This is an application to webscrape subreddit posts, then create simple wordmaps. The webscrapper applies simple rate limiting with python's time.sleep() command. It also uses the Tor service for proxy rotation. 


## Dependencies
### Python Modules
  * Wordcloud
  * Pandas
  * Stem 
### Other 
  * Python 3.7
  * Spyder
  * Tor Service
  
## Run
```
#Webscrape a subreddit
sudo ./redditscrape.py <subreddit-name> <number-of-pages-to-scrape>
```

# To Add On
These are just some other ideas I have for improving the application:
  * apply sentimental analysis
  * weigh words by the post's likes count
  * apply other data visualization techniques such as word clustering
  * apply other text preprocessing techniques such as lemmatization
