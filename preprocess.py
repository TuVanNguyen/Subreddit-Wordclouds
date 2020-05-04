#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:17:36 2020

@author: tuvan
"""
#Reference: https://www.kdnuggets.com/2019/04/text-preprocessing-nlp-machine-learning.html

import pandas as pd
import re
from nltk.corpus import stopwords
import json
import sys

class Preprocessor:
    def __init__(self,filename):
        self.file = filename
        self.subreddit = filename[5:-5] 
        self.data = None
        self.text = ""
    
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
    
    def lowercase(self):
        """
        Description
        -------
        turns all text to lowercase
        
        Returns
        -------
        None.

        """
        self.text = self.text.lower()
    
    def remove_noise(self):
        """
        Description
        -------
        removes punctuation
        
        Returns
        -------
        None.

        """
        self.text = re.sub(r'[^\w\s]',' ',self.text)
        self.text = re.sub(r' r ', ' r/',self.text)
        
    def remove_stopwords(self):
        words = self.text.split()
        #print(stopwords.words('english'))
        #self.text = "".join()
        mystopwords = stopwords.words('english')
        morestops = ["(self."+self.subreddit.lower()+")", "also", "like",
                     "would","much", "still", "thing", "things", "something"]
        mystopwords += morestops
        
        self.text = "".join(word+" " for word in words if word not in mystopwords)
        
    def clean(self):
        self.aggregate()
        self.lowercase()
        self.remove_stopwords()
        self.remove_noise()
        self.remove_stopwords()
    
if __name__ == "__main__":
    """
    Inputs:
    [1]: filename
    """
    #Testing
    filename =  sys.argv[1]
    subreddit_preprocessor = Preprocessor(filename)
    subreddit_preprocessor.clean()
    print(subreddit_preprocessor.text)
