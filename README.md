# StreamlitTTS
This Streamlit app allows you to convert text to audio files using the Microsoft Edge's online text-to-speech service.

[Have a Try](https://shangfr-streamlittts-app-xvews2.streamlit.app/)

App preview:
![Screenshot1](./image.png?raw=true "Screenshot1")

## Features
Access to most of the Microsoft Edge's TTS API features, including
- voice and language selection
- voice tuning (speaking rate & volume)
- audio formats (MP3 [.mp3])
- audio captions

You can play the audio from the converted text directly in the browser or download the audio file to your local machine.


## Installation
Clone this repository
```bash
git clone https://github.com/shangfr/StreamlitTTS.git
```
Install the Python requirements using the requirements.txt file. This will install Streamlit, the edge-tts Python package, and other dependencies.
```bash
pip install -r requirements.txt
```

## Run the Streamlit app
```bash
streamlit run app.py
```
This command will start the streamlit app, will automatically open a browser window, and navigate to http://localhost:8501/
