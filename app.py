import requests, re, os, base64  
from logger import logger 
from flask import Flask, request 
from pytube import extract
import banana_dev as banana
from doctr.io import DocumentFile  
from doctr.models import ocr_predictor
from youtube_transcript_api import YouTubeTranscriptApi


app = Flask(__name__)
model = ocr_predictor(pretrained=True)   

@app.route('/')
def hello(): 
  return "your app is running!"

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
        logger.info(f"Transcript found: \n\n{text}")

        return text
    except: 
        # logger.info(f"Transcript not found for this link: {link}, so passing to 🍌")
        API_KEY = "ec49909f-3d2f-4044-8882-535e3ce8a383"
        MODEL_KEY = "7734639e-bcae-41f6-b7b9-47a9cbba26e1"
        payload = {'link': link}
        out = banana.run(API_KEY, MODEL_KEY, payload)
        out = out['modelOutputs'][0]['text']
        logger.info(f"Transcript from the 🍌: \n\n{out}")

        return out 


def file_txt(file, types) -> str: 
    file = base64.b64decode(file)
    if types == 'PDF': 
      doc = DocumentFile.from_pdf(file)
    if types == 'IMAGE': 
      doc = DocumentFile.from_images(file) 

    result = model(doc)
    text = result.render()
    text = text.replace('\n', '')

    return text

  
def api_giver(text:str, condition='FILL'): 
    if condition == 'FILL': 
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

      
@app.route('/text_to_question', methods = ['POST', 'GET'])     
def exectuter(): 
    ins = request.args.get('input')
    condition = request.args.get('condition')
    types = request.args.get('type')
    file_type = request.args.get('file_name')

    if file_type.endswith('.pdf'): file_type = 'PDF'; 
    else: file_type = 'IMAGE'

    logger.info(f"Got the I/s \ninput: {ins}\ncondition: {condition}\ntype: {types}")

    if types == 'TEXT': 
      logger.info("Type: TEXT: sent directly to BANANA")
      out = api_giver(text = ins, condition = condition) 
     
    if types == 'VIDEO': 
      logger.info("Type: VIDEO: sent the video to youtube function")
      text = yt_text(ins) 
      out = api_giver(text = text, condition = condition) 
      
    if types == 'DOCUMENT': 
      logger.info("Type: PDF/IMAGES: sent the link to doctr")
      text = file_txt(ins, file_type)
      out = api_giver(text = text, condition = condition) 

    return out 
      
    
if __name__ == '__main__': 
  app.run()
  
