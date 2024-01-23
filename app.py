# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:38:32 2023

@author: shangfr
"""
    
import io
import os
import streamlit as st
from PIL import Image
from tts_script import tts
from movie import MP324

if "complete" not in st.session_state:
    st.session_state.complete = False

base_dir = 'voices'
files = os.listdir(base_dir)

st.subheader("🎧 :orange[文本转语音]")
st.caption("Microsoft Edge's online text-to-speech service.")

col00, col01, col02 = st.columns([2,3,5])

area = col00.selectbox(
    "地区 👇",
    ["CN", "HK", "TW"],
    key="visibility"
)

sex = col01.selectbox(
    "性别 👇",
    ["male", "female"]
)

fa = [f for f in files if f.split('-')[1] == area]
fb = [f for f in fa if f.split('_')[0] == sex]

sex_emoji = sex.replace('female', '👩').replace('male', '🧑')
voice = col02.selectbox(f"主播 {sex_emoji}", fb)
#[f.split('_')[1].split('.')[0].split('-')[-1] for f in fb]
with open(os.path.join(base_dir, voice), 'rb') as audio_file:
    audio_bytes = audio_file.read()
st.audio(audio_bytes, format="audio/mp3")

with st.form("my_form"):


    txt = st.text_area(':green[**在线文字转语音**]', '''制作教程
    ⚙️ 步骤1：在这里输入或者粘贴要转换的文本
    ⚙️ 步骤2：选择你想要的不同语音配置
    ⚙️ 步骤3：点击合成
    ''', height=300)
    
    col1, col2 = st.columns(2)
    rate = col1.slider(f'{sex_emoji} 语速', -50, 50, 0)
    volume = col2.slider(f'{sex_emoji} 音量', -50, 50, 0)
    voice = voice.split('_')[1].split('.')[0]
    
    submitted = st.form_submit_button('⚙️ 合成', use_container_width=True, help='语音合成')
    if submitted:
        with st.spinner('正在合成...'):
            if tts(voice, txt, rate, volume):
                st.session_state.complete = True

if not st.session_state.complete:
    st.warning('请先点击⚙️进行语音合成。', icon="👆")
    st.stop()

with open('output/audio.mp3', 'rb') as audio_file:
    audio_bytes = audio_file.read()

with open('output/audio.vtt', 'r', encoding='UTF-8') as caption_file:
    captions = caption_file.read()

col11, col12, col13 = st.columns([8, 1, 1])
col11.success('文本转语音已完成。', icon="👇")
col12.caption('')
col13.caption('')
col12.download_button('📥', audio_bytes, file_name='audio.mp3', help='音频下载')
col13.download_button('🧾', captions, file_name='audio.vtt', help='字幕下载')

st.audio(audio_bytes, format="audio/mp3")


container = st.container()
uploaded_files = st.file_uploader(
    "上传图片", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

image_list = list()
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    # .resize((800, 800), Image.ANTIALIAS)
    image = Image.open(io.BytesIO(bytes_data))
    image_list.append(image)


# Invoking the parameterized constructor of the MP3ToMP4 class.
if len(image_list)== 0:
    container.warning('上传图片进行视频合成。', icon="👇")
    st.stop()

movie = st.button('⚙️ 合成视频', use_container_width=True, help='语音合成')
title = 'TESTTESTTEST'
output_folder_path = "output"

if movie:
    with st.spinner('正在合成...'):
        MP324(image_list,title, output_folder_path)

with open(output_folder_path+'/video.mp4', 'rb') as video_file:
    video_bytes = video_file.read()

st.video(video_bytes)
