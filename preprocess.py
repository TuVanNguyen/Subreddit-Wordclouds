#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:17:36 2020

@author: tuvan
"""
#Reference: https://www.kdnuggets.com/2019/04/text-preprocessing-nlp-machine-learning.html
#Reference: https://www.datacamp.com/community/tutorials/stemming-lemmatization-python

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import json
import sys

class Preprocessor:
    def __init__(self,filename):
        self.file = filename
        self.subreddit = filename[5:-5] 
        self.data = None
        self.text = ""
        self.titles_only = ""
    
    def aggregate(self):
        """
        Description
        -------
        take all the text from the json file and aggregate all the text from 
        the titles and content into a single string
        
        Returns
        -------
        None.
        """
        with open(self.file, 'r') as f:
            self.data = json.load(f)
        
        df = pd.DataFrame(self.data['data'][1])
        self.text = "".join(post_title+ "\n"+ post_content for post_title, post_content in zip(df.title,df.content))
        self.titles_only = "".join(post_title+ "\n" for post_title in df.title)
    
    def lowercase(self,text):
        """
        Description
        -------
        turns all text to lowercase
        
        Returns
        -------
        None.

        """
        text = text.lower()
        return text
    
    def remove_noise(self,text):
        """
        Description
        -------
        removes punctuation
        
        Returns
        -------
        None.

        """
        text = re.sub(r'[^\w\s]',' ',text)
        text = re.sub(r' r ', ' r/',text)
        return text


    def remove_stopwords(self,text):
        words = text.split()
        #print(stopwords.words('english'))
        #self.text = "".join()
        mystopwords = stopwords.words('english')
        morestops = ["(self."+self.subreddit.lower()+")", "also", "like",
                     "would","much", "still", "thing", "things", "something",
                     "lot", "really", "around", "always", "even", "well",
                     "one", "anyone", "already", "within", "yet", "upon", "towards",
                     "please", "may", "someone", "anything", "maybe"]
        mystopwords += morestops
        
        text = "".join(word+" " for word in words if word not in mystopwords)
        return text

    def lemmatize(self,text):
        """
        Description
        -------
        removes punctuation
        
        Returns
        -------
        None.

        """
        wordnet_lemmatizer = WordNetLemmatizer()
        sentence_words = nltk.word_tokenize(text)
        lematized_string = "".join(wordnet_lemmatizer.lemmatize(word,pos="v")+" " for word in sentence_words)
        text = lematized_string
        return text
        #print(sentence_words)

        
    def clean(self):
        self.aggregate()
        
        self.text = self.lowercase(self.text)
        self.text = self.remove_stopwords(self.text)
        self.text = self.remove_noise(self.text)
        self.text = self.remove_stopwords(self.text)
        self.text = self.lemmatize(self.text)
        
        self.titles_only = self.lowercase(self.titles_only)
        self.titles_only = self.remove_stopwords(self.titles_only)
        self.titles_only = self.remove_noise(self.titles_only)
        #self.titles_only= self.remove_stopwords(self.titles_only)
        self.titles_only = self.lemmatize(self.titles_only)
        
if __name__ == "__main__":
    """
    Inputs:
    [1]: filename
    """
    #Testing
    filename =  sys.argv[1]
    subreddit_preprocessor = Preprocessor(filename)
    subreddit_preprocessor.clean()
    print(subreddit_preprocessor.titles_only)
