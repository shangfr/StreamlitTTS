# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 15:21:06 2023

@author: shangfr
"""
import asyncio
import edge_tts

async def async_function(voice,text,rate,volume,webvtt='output/caption.vtt',output_file='output/audio.mp3') -> None:
        rate = f"{rate}%"
        volume = f"{volume}%"
        communicate = edge_tts.Communicate(text, voice,rate=rate,volume=volume)
        submaker = edge_tts.SubMaker()
        with open(output_file, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    
        with open(webvtt, "w", encoding="utf-8") as file:
            file.write(submaker.generate_subs())


def tts(voice,txt,rate,volume):
    if rate>=0:
        rate = '+'+str(rate)
    if volume>=0:
        volume = '+'+str(volume)
        
    try:                
        asyncio.get_event_loop().run_until_complete(
            async_function(voice, txt, rate=rate, volume=volume))
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.get_event_loop().run_until_complete(async_function(voice,txt,rate=rate,volume=volume))
    
    return True