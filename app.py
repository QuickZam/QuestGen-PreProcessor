from flask import Flask 
from logger import logger 
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi


app = Flask(__name__)

def yt_text(link:str) -> str: 
    """Inputs the youtube link and outputs the transcription of the link"""
    video_id = extract.video_id(link)

    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = ' '.join([ i['text'].replace('\n', '') for i in transcript])
    
    print(text)

    return transcript



yt_text("https://www.youtube.com/watch?v=1H-slVEJcN4")