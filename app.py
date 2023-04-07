# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:38:32 2023

@author: shangfr
"""
import os
import streamlit as st
from tts_script import tts

if "complete" not in st.session_state:
    st.session_state.complete = False

base_dir = 'voices'
files = os.listdir(base_dir)

with st.sidebar:
    st.subheader(":orange[文本转语音]")
    st.caption("Microsoft Edge's online text-to-speech service.")

    area = st.radio(
        "地区 👇",
        ["CN", "HK", "TW"],
        key="visibility",
        horizontal=True
    )

    sex = st.radio(
        "性别 👇",
        ["male", "female"],
        horizontal=True
    )

    fa = [f for f in files if f.split('-')[1] == area]
    fb = [f for f in fa if f.split('_')[0] == sex]

    sex_emoji = sex.replace('female', '👩').replace('male', '🧑')
    voice = st.selectbox(f"主播 {sex_emoji}", fb)
    #[f.split('_')[1].split('.')[0].split('-')[-1] for f in fb]
    with open(os.path.join(base_dir, voice), 'rb') as audio_file:
        audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")


txt = st.text_area(':green[**在线文字转语音**]', '''制作教程
⚙️ 步骤1：在这里输入或者粘贴要转换的文本
⚙️ 步骤2：选择你想要的不同语音配置
⚙️ 步骤3：点击合成
''', height=300)

col1, col2 = st.columns(2)

rate = col1.slider(f'{sex_emoji} 语速', -50, 50, 0)
volume = col2.slider(f'{sex_emoji} 音量', -50, 50, 0)

voice = voice.split('_')[1].split('.')[0]

if col1.button('⚙️', help='语音合成'):
    with st.spinner('正在合成...'):
        if tts(voice, txt, rate, volume):
            st.session_state.complete = True

if not st.session_state.complete:
    col1.warning('请先点击⚙️进行语音合成。', icon="👆")
    st.stop()
else:
    col1.success('语音合成已完成，点击试听。', icon="👇")
    with open('output/test.mp3', 'rb') as audio_file:
        audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    with open('output/字幕.vtt', 'r', encoding='UTF-8') as caption_file:
        captions = caption_file.read()

    col2.download_button(
        label='💠',
        data=captions,
        file_name='字幕.vtt',
        help='字幕下载'
    )
    col2.success('语音字幕已完成，点击下载。', icon="👆")
