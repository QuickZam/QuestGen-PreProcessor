import requests, re, os 
from flask import Flask 
from pytube import extract
import banana_dev as banana
from doctr.io import DocumentFile  
from doctr.models import ocr_predictor
from youtube_transcript_api import YouTubeTranscriptApi


app = Flask(__name__)
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
        # text = re.sub('[^a-zA-Z0-9]', ' ', text)
        # text = request_api(text)
        # logger.info(f"Transcript found: \n\n{text}")

        return text
    except: 
        # logger.info(f"Transcript not found for this link: {link}, so passing to 🍌")
        payload = {'link': link}
        out = banana.run(API_KEY, MODEL_KEY, payload)
        # logger.info(f"Transcript from the 🍌: \n\n{out}")

        return out 

def file_txt(file) -> str: 
    if file.endswith('.pdf'): 
      doc = DocumentFile.from_pdf(file)
    elif file.endswith(('.png', '.jpeg', 'jpg')): 
      doc = DocumentFile.from_images(file) 
    else: 
      text = 'Please provide pdf or img format'
      return text 

    result = model(doc)
    text = result.render()
    text = text.replace('\n', '')

    return text

  
def api_giver(text:str, condition='TrueOrFalse'): 
    if condition == 'TrueOrFalse': 
        api_key = "ec49909f-3d2f-4044-8882-535e3ce8a383"
        model_key = "389eaf12-4801-4673-bd57-52140c4cc90c"
        payload = {"text": text}
        out = banana.run(api_key, model_key, payload)
        out = out['modelOutputs'][0]['html']

        return out 

    if condition == 'MCQ': 
        api_key = "ec49909f-3d2f-4044-8882-535e3ce8a383"
        model_key = "ddd49032-854c-4bb3-a368-9fd5b8c85646"

        payload = {"text": text, "condition" : False}
        out = banana.run(api_key, model_key, payload)
        out = out['modelOutputs'][0]['output'][0]
        
        return out
      
 def exectuter(ins:str, condition:str, type:str): 
    if type == 'TEXT': 
      out = api_giver(text = ins, condition = condition) 
     
    if type == 'VIDEO': 
      text = yt_text(ins) 
      out = api_giver(text = text, condition = condition) 
      
    if type == 'PDF': 
      text = file_txt(ins)
      out = api_giver(text = in, condition = condition) 
      
    return out 
      
    
    
    
    
    
    
