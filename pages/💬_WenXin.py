# -*- coding: utf-8 -*-
"""
Created on Tue May  9 18:41:01 2023

@author: shangfr
"""

import wenxin_api # 可以通过"pip install wenxin-api"命令安装
from wenxin_api.tasks.text_to_image import TextToImage
wenxin_api.ak = "PjVnqcfqeTOxEPUHKSuyX1gGOnAb8sFG"
wenxin_api.sk = "ajVLcITbuf4hhHdMAFzg0k4PGHcdRGjI"
num = 2
input_dict = {
    "text": "睡莲",
    "style": "油画",
    "resolution":"512*512",
    "num": num
}
rst = TextToImage.create(**input_dict)
print(rst)