# loic.berthod@hevs.ch /lberthod@gmail.com
 # python script : openai chatgpt 3-5, whister, pyttsx3, ai text to speak
 # do the pip install you need
 # need to have a chatbot.txt et openaiapikey.txt
 
import sounddevice as sd
import soundfile as sf
import numpy as np
import openai
import os
import requests
import re
from colorama import Fore, Style, init
import datetime
import base64
from pydub import AudioSegment
from pydub.playback import play
import time
 
import pyttsx3
engine = pyttsx3.init() # object creation]
 
""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 245)     # setting up new voice rate
voices = engine.getProperty('voices')
 
"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
 
"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female
 
for n in range(0, len(voices)): 
    print(n, voices[n])
 
init()
# Typical non-streaming request
start_time = time.time()
 
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
 
api_key = "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"
 
conversation1 = []  
chatbot1 = open_file('chatbot.txt')
 
def chatgpt(api_key, conversation, chatbot, user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):
    openai.api_key = api_key
    conversation.append({"role": "user","content": user_input})
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": chatbot}]
    messages_input.insert(0, prompt[0])
 
    response = openai.ChatCompletion.create(
 
        model='gpt-3.5-turbo',
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input,
        stream=True
    )
 
    collected_chunks = []
    collected_messages = []
    temp = 0
    lenA = 0
    for chunk in response:
        chunk_time = time.time() - start_time
        collected_chunks.append(chunk)
        chunk_message = chunk['choices'][0]['delta']
        collected_messages.append(chunk_message)
        print(time.time())
        print(chunk_message)
        temp = temp + 1
        print(temp)
        if 'content' in chunk_message:
            if "." in chunk_message.content or "?" in chunk_message.content or "!" in chunk_message.content or "," in chunk_message.content:
                full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
                print(f"Full conversation received: {full_reply_content}")
                nouvelle_chaine = full_reply_content[lenA:]
                lenA = len(full_reply_content)
                print(len(nouvelle_chaine))    
 
                engine.say(nouvelle_chaine)
                engine.runAndWait()
                engine.stop()
            else : temp= 1
 
    full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
    print(f"Full conversation received: {full_reply_content}")
    return full_reply_content
 
def record_and_transcribe(duration=8, fs=44100):
    print('Recording...')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    print('Recording complete.')
    filename = 'myrecording.wav'
    sf.write(filename, myrecording, fs)
    with open(filename, "rb") as file:
        openai.api_key = api_key
        result = openai.Audio.transcribe("whisper-1", file)
    transcription = result['text']
    print(transcription)
    return transcription
 
while True:
    user_message = record_and_transcribe()
    chatgpt(api_key, conversation1, chatbot1, user_message)
 
 
