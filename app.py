import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

google_api_key =os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
model=genai.GenerativeModel("gemini-1.5-flash")

input_prompt="""
  You are a professional YouTube video summarizer. 
  Your role is to take the provided transcript and 
  generate a concise, yet thorough summary of the video.
    Summarize the key points, main ideas, and any critical information, 
    ensuring that the summary is structured in bullet points. The summary should 
    be no longer than 250 words and provide a clear understanding of the video's content.

The transcript text will be appended below:
"""
def extract_transcript(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""

        for i in transcript_text:
            transcript+=" "+i["text"]

        return transcript
    except Exception as e :
        raise e
 



def get_response(transcript,input_prompt):
    response = model.generate_content(input_prompt+transcript)
    return response.text


st.set_page_config(page_title="Youtube Video Summarizer")
st.header("Youtube Video to Notes")

link=st.text_input("Provide the link of the video: ")

if link:
    video_id=link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=False,width=300)

if st.button("Get Notes"):
    transcript=extract_transcript(link)
    if transcript:
        res=get_response(transcript=transcript,input_prompt=input_prompt)
        st.write("Your Notes Ojou: ")
        st.write(res)

