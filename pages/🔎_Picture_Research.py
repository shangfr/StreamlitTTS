# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:37:08 2023

@author: shangfr
"""

import streamlit as st
from pexels import search

txt = st.text_area(':orange[**在线图片搜索**]', '', height=100)

if txt:
    url_lst = search(txt)
    
    md_img = [f"![图片]({url})" for url in url_lst]
    
    st.markdown('\n\n'.join(md_img))
