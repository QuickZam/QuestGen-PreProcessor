import requests, re 
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
model = ocr_predictor(pretrained=True)   


def request_api(summa): 
  # https://curlconverter.com/
  # http://bark.phon.ioc.ee/punctuator

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',}

  data = f"text={summa}"
  response = requests.post('http://bark.phon.ioc.ee/punctuator', headers=headers, data=data)
  print(response)
  print(response.text)

  return response.text


def yt_text(link:str) -> str: 
    """Inputs the youtube link and outputs the transcription of the link"""
    try: 
        video_id = extract.video_id(link)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([ i['text'].replace('\n', '') for i in transcript])
        text = re.sub('[^a-zA-Z0-9]', ' ', text)
        # text = request_api(text)
        logger.info(f"Transcript found: \n\n{text}")

        return text
    except: 
        logger.info(f"Transcript not found for this link: {link}, so passing to 🍌")
        payload = {'link': link}
        out = banana.run(API_KEY, MODEL_KEY, payload)
        logger.info(f"Transcript from the 🍌: \n\n{out}")

        return out 

def file_txt(file) -> str: 
    if file.name.endswith('.pdf'): 
      doc = DocumentFile.from_pdf(file.read())
    elif file.name.endswith(('.png', '.jpeg', 'jpg')): 
      doc = DocumentFile.from_images(file.read()) 
    else: 
      text = 'Please provide pdf or img format'
      return text 

    result = model(doc)
    text = result.render()

    return text


if __name__ == "__main__": 
  app.run()
