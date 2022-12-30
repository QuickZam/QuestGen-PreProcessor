import requests 
from flask import Flask 
from logger import logger 
from pytube import extract
import banana_dev as banana
from doctr.io import DocumentFile  
from doctr.models import ocr_predictor
from youtube_transcript_api import YouTubeTranscriptApi


app = Flask(__name__)
API_KEY = "ec49909f-3d2f-4044-8882-535e3ce8a383"
MODEL_KEY = "7734639e-bcae-41f6-b7b9-47a9cbba26e1"

def request_api(summa): 
  # https://curlconverter.com/
  # http://bark.phon.ioc.ee/punctuator

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',}

  data = f"text={summa}"
  response = requests.post('http://bark.phon.ioc.ee/punctuator', headers=headers, data=data)

  return response.text


def yt_text(link:str) -> str: 
    """Inputs the youtube link and outputs the transcription of the link"""
    try: 
        video_id = extract.video_id(link)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([ i['text'].replace('\n', '') for i in transcript])
        text = request_api(text)
        logger.info(f"Transcript found: \n\n{text}")

        return text
    except: 
        logger.info(f"Transcript not found for this link: {link}, so passing to 🍌")
        payload = {'link': link}
        out = banana.run(API_KEY, MODEL_KEY, payload)
        logger.info(f"Transcript from the 🍌: \n\n{out}")

        return out 

def file_txt(file) -> str: 
    


# yt_text("https://www.youtube.com/watch?v=1H-slVEJcN4")
request_api("""Wait a minute I think I left my conscience on your front doorstep, oh oh Wait a minute I think I left my consciousnessin the sixth dimension But I'm here right now, right now Just sitting in a cloud, oh wow I'm here right now,right now with you, oh wow, oh wow I don't even care,I’ll run my hands through your hair You wanna run your fingers through mine But my dreads too thick and that's alright Hold on, wait a minute,Feel my heart's intention, oh Hold on, wait a minute,I left my consciousness in the sixth dimension Left my soul in his vision Let's go get it, oh, oh,Let's go get it, oh, oh Some things don't work,Some things are bound to be Some things, they hurt,And they tear apart me You left your diary at my house And I read those pages,do you really love me, baby? Some things don't work,Some things are bound to be Some things, they hurt,And they tear apart me But I broke my word,and you were bound to see And I cried at the curb,When you first said, "Oel ngati kameie" Hold on, wait a minute,Feel my heart's intention Hold on, wait a minute I left my consciousness in the sixth dimension,Left my soul in his vision Let's go get it, oh, oh,Let's go get it, oh, oh Some people like to live Some just tryin' to get by Some people like that hurt Some just rather say goodbye, bye Hold on, wait a minute,Feel my heart's intention, oh Hold on, wait a minute,I left my consciousness in the sixth dimension Left my soul in his vision Let's go get it, ah, ah,Let's go get it, ah, ah (Let's go get it) (Mmh) (Let's go get it) (Mmh)""")

