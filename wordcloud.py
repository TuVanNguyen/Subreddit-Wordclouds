#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 09:29:19 2020

@author: tuvan
"""
#Reference: https://www.datacamp.com/community/tutorials/wordcloud-python

import preprocess
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import sys
import matplotlib.pyplot as plt

class MyWordCloud:
    def __init__(self,text,subreddit):
        self.text = text
        self.wordcloud = None
        self.subreddit = subreddit
        self.outputfile = "wordmaps/"+subreddit+".png"
    def generate(self):
        mystopwords = set(STOPWORDS)
        mask = np.array(Image.open("snoo.png"))
        self.wordcloud = WordCloud(stopwords=mystopwords, mask=mask,
                                   background_color="white",mode="RGBA",
                                   max_words=1000).generate(self.text)
        plt.imshow(self.wordcloud, interpolation = 'bilinear')
        plt.axis("off")
        plt.figure()
        #plt.savefig(self.outputfile, format="png")
        #plt.imshow(mask)
        plt.show()
    
if __name__ == "__main__":
    """
    Inputs:
    [1]: filename of webscrapped json data
    """
    #Testing
    filename =  sys.argv[1]
    r_preprocessor = preprocess.Preprocessor(filename)
    r_preprocessor.clean()
    r_wordcloud = MyWordCloud(r_preprocessor.text, r_preprocessor.subreddit)
    r_wordcloud.generate()