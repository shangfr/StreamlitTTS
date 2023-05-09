# -*- coding: utf-8 -*-
"""
Created on Tue May  9 17:11:42 2023

@author: shangfr
"""
import jieba.analyse
# Import API class from pexels_api package
from pexels_api import API
# Type your Pexels API
PEXELS_API_KEY = 'a5Ki4wV7ok8ETkiqRonkUqXeGuCZHXJNXnCL5Q2crR70ownyemOPD7fz'
# Create API object
api = API(PEXELS_API_KEY)
# Search five 'kitten' photos

def search(txt,k=10):
    url_lst = []
    keywords = jieba.analyse.extract_tags(txt, topK=k)
    for k in keywords:
        api.search(k , page=1, results_per_page=5)
        # Get photo entries
        photos = api.get_entries()
        # Loop the five photos
        for photo in photos:
          url_lst.append(photo.medium)
          
    return url_lst
      
      
      
