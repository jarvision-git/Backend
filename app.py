from flask import Flask, request, jsonify, session, Response
from flask_session import Session

import jsonpickle
import json
from datetime import timedelta

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.secret_key = 'billorani'
app.permanent_session_lifetime = timedelta(days=5)  # Set session timeout

import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key="AIzaSyAiU1xIWXdK3lLlgdCDIRIjISkVMdEoWpU")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[]
)

@app.route("/", methods=['POST'])
def index():
    if request.method == 'POST':
        content_pickle = session.get('gemini detective game data')
        if content_pickle:
          chat_session.history = (jsonpickle.decode(content_pickle))
        else:
          print("No data found")
          
        data = request.get_json()
        
        message = data.get('message')
        print('Received message:', message)
        
        response = ""
        while not response:
          response = chat_session.send_message(message)
          
        session['gemini detective game data'] = jsonpickle.encode(chat_session.history)
        y = (response.text)
        response_obj = Response(y, content_type="application/json")
        print(y)
        return response_obj
    else:
        return("No msg received")
    
@app.route("/restart", methods=['POST'])
def restart():
    session.clear()
    print("Cookies cleared")
    chat_session = model.start_chat(history=[])
    return ("restart")

@app.route("/hint", methods=['POST'])
def hint():
    if request.method == 'POST':
        data = request.get_json()
        
        message = data.get('message')
        print('Received message:', message)
        response = chat_session.send_message(message)
        y = (response.text)
        print(y)
        return y
    else:
        return("No msg received")

if __name__ == '__main__':
    app.debug = True
    app.run()
