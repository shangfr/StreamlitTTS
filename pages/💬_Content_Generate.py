# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:37:08 2023

@author: shangfr
"""

import openai
import streamlit as st


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""


openai.api_key = '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'

@st.cache_resource
def answer_ChatGPT(question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0.2,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return response.choices[0].text


@st.cache_resource
def image_create(PROMPT):
    response = openai.Image.create(
        prompt=PROMPT+"——超现实主义，色彩柔和，细节丰富。",
        n=1,
        size="512x512",
    )

    return [r["url"] for r in response["data"]]


def input_and_clear():
    st.session_state['user_input'] = st.session_state['input']
    st.session_state['input'] = ""

# layout
st.header("🔬 ChatGPT Demo")

if st.session_state['user_input']:
    try:
        output = answer_ChatGPT(st.session_state['user_input'])
    except:
        output = 'error'
    st.session_state.past.append(st.session_state['user_input'])
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        st.info(st.session_state['past'][i], icon="🤶")
        ans = st.session_state["generated"][i]
        if ans == 'error':
            st.error('网络错误，请再试一遍。', icon="🤖")
            st.session_state["generated"].pop(i)
            st.session_state['past'].pop(i)
        else:
            st.success(ans, icon="🤖")
            
            ans_list = ans.split("。")
            if len(ans_list)>5:
                ans_list = ans_list[:5]
            for PROMPT in [r for r in ans_list if r.strip()]:
                url_lst = image_create(PROMPT)
                
            md_img = [f"![图片]({url})" for url in url_lst]
            st.markdown('\n\n'.join(md_img))

st.text_input("**请输入问题 👇**", key="input", on_change=input_and_clear)