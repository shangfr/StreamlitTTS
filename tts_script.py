# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 15:21:06 2023

@author: shangfr
"""
import asyncio
import edge_tts


async def async_function(voice, text, rate, volume, webvtt='output/audio.vtt', output_file='output/audio.mp3') -> None:
    rate = f"{rate}%"
    volume = f"{volume}%"
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
    submaker = edge_tts.SubMaker()
    with open(output_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub(
                    (chunk["offset"], chunk["duration"]), chunk["text"])

    with open(webvtt, "w", encoding="utf-8") as file:
        content = submaker.generate_subs()
        file.write(content.replace("\r",""))


def tts(voice, txt, rate, volume):
    if rate >= 0:
        rate = '+'+str(rate)
    if volume >= 0:
        volume = '+'+str(volume)

    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_function(voice, txt, rate=rate, volume=volume))

    return True

def convert_text_to_speech(text, output_file="test"):
    import os
    import subprocess
    
    output_directory = "output"
    os.makedirs(output_directory, exist_ok=True)

    # 执行命令，并将工作目录设置为输出目录
    try:
        command = ['edge-tts', '--voice', 'zh-CN-XiaoyiNeural', '--text', text, '--write-media', f'{output_file}.mp3', '--write-subtitles', f'{output_file}.vtt']
        result = subprocess.run(command, cwd=output_directory, timeout=10)

    except subprocess.CalledProcessError as e:
        print("Command execution failed with return code:", e.returncode)
        print("Command output:", e.output)


filename = "output/audio.vtt"

def file_to_subtitles(filename):
    import webvtt
    """ Converts a srt file into subtitles.

    The returned list is of the form ``[((ta,tb),'some text'),...]``
    and can be fed to SubtitlesClip.

    Only works for '.srt' format for the moment.
    """
        
    times_texts = []
    current_times = None
    current_text = ""
    
    subtitles = webvtt.read(filename)

    for subtitle in subtitles:
        current_times = [subtitle.start_in_seconds,subtitle.end_in_seconds]
        current_text = subtitle.text.strip('\n')
        times_texts.append((current_times, current_text))
 
    return times_texts

