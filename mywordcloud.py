#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 09:29:19 2020

@author: tuvan
"""
#Reference: https://www.datacamp.com/community/tutorials/wordcloud-python

import preprocess
from wordcloud import WordCloud, STOPWORDS
import sys
import matplotlib.pyplot as plt

class MyWordCloud:
    def __init__(self,text,filename):
        self.text = text
        self.wordcloud = None
        self.outputfile = "wordmaps/"+filename+".png"
    def generate(self):
        mystopwords = set(STOPWORDS)
        self.wordcloud = WordCloud(stopwords=mystopwords).generate(self.text)
        fig = plt.figure(frameon=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(self.wordcloud, interpolation = 'bilinear', aspect='auto')
        plt.axis("off")
        fig.savefig(self.outputfile, format="png")
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
    r_wordcloud = MyWordCloud(r_preprocessor.text, r_preprocessor.subreddit )
    r_wc_titles = MyWordCloud(r_preprocessor.titles_only, r_preprocessor.subreddit + "_titles")
    r_wordcloud.generate()
    r_wc_titles.generate()