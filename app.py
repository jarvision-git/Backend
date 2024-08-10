from flask import Flask, request, jsonify,session
import jsonpickle

import json
from flask_cors import CORS, cross_origin



from datetime import timedelta



app = Flask(__name__)
CORS(app)

app.secret_key = 'billorani'
app.permanent_session_lifetime = timedelta(days=5)  # Set session timeout

import os

import google.generativeai as genai

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
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="""I want to develop a user centric detective game that has gemini at its back end and develops the game plot according to user prompts.
The user is explained the initial game scenario via a text based description. The user can then interrogate suspects to uncover new clues and suspects . The game has various location. The is prominently text based that is user can interact only through chat and gemini responds through chat itself. The game story should be layered and extensive so that user spends some time before finishing the game.

You have to act out every character in the story. Feel free to add any plot twists. You also have to provide the initial scenario and the characters

To indicate which message is meant for which character, the text will be prefixed with character name. Only respond as that character and no one else.

General Instructions 

on prompting start, provide the initial scenario and provide the list of current suspects based on people directly linked to the crime scene. Also state the purpose of solving the murder in the scenario. Then keep expanding the suspects based on how player unfolds the story. The game has 3 difficulty levels easy , medium, hard. The easy difficulty setting must have a simpler story where as hard difficulty should have a complex and convoluted story that takes time and efforts to solve. The story for the game will also be provided at the start 

Try to provide character responses only in the form of dialogue.

Maintain a list of suspects available for interrogation after every response. Keep Inspector in list all the time . Also the list must be consistent. The names must be same. 

The player is to be called Detective all the time. 

Mention the steps available like examining the crime scene, looking or clues in the ofice, etc.


JSON structure should be suspects - for list of current suspects ,available_actions - actions that can be done in current scenario, and response for response to prompt. also return a key speaker, denoting who the response is from. The speaker name must be the same as in suspects list. Do not include the speaker name in the response value. Also include a key win which is set to zero and turns 1 only if the player finds the culprit with sufficient proof and the culprit accepts the verdict.

The json response in start command should have the initial scenario explained in the response key and keep the speker key as empty along with otherjson attiributes.

on receiving #1ad57b3o0 get hint as prompt, return a json object with hint as key and describe the hint and available_actions as key and actions that the player can take in current scenario



The stories are as follows:

Story 1 :
## The Neo-Victorian Murder

*Central Mystery:* The prestigious Professor Alistair Crowley, a pioneer in chrono-mechanics (the study of time manipulation), has been found murdered in his opulent laboratory located in the prestigious Aether District of Neo-Victoria.  

*World Setting:*

* Neo-Victoria: A sprawling metropolis inspired by Victorian England, but infused with fantastical steampunk technology. Think airships, clockwork automatons, and gaslight lamps alongside horse-drawn carriages and grand architecture.  
* Society: Neo-Victoria is divided by class. The affluent elite reside in the Aether District, powered by aetherium, a mysterious energy source that fuels technology.  The underbelly, known as the Cogs, houses the working class who toil in factories fueled by coal. Tensions simmer between the classes. 
* Historical Event: The Great Clockwork Uprising (50 years ago) saw clockwork automatons used as laborers rebel against their human masters. Though quelled, the event left a lasting scar on society, with lingering mistrust towards automatons.

*Characters:*

* *The Victim:* Professor Alistair Crowley (50s) - A brilliant but arrogant scientist obsessed with time travel. He had recently announced a breakthrough that could supposedly send messages to the past.  
* *Suspects:*
    * *Lady Lavinia Cavendish (40s):* Professor Crowley's estranged wife, known for her lavish lifestyle and gambling debts. Motive: Potential inheritance and spite. 
    * *Dr. Thaddeus Kensington (30s):* A brilliant but envious colleague of Professor Crowley. Motive: Professional rivalry and a desire for Crowley's research.  
    * *Inspector Bartholomew Gearsmith (60s):* A grizzled veteran detective with a distrust of new technology. Motive: Skeptical of Professor Crowley's work and frustrated by his lack of cooperation. 
    * *Fidget (unknown age):* A mischievous automaton assistant who worked in Professor Crowley's lab. Motive: Unknown, but some automatons still harbor resentment towards humans. 

*Story Layers:*

* *Professor Crowley's Secret Project:* Gemini can uncover clues hinting at Professor Crowley's true research - not time travel, but a way to manipulate causality. This could be a dangerous invention with unforeseen consequences.  
* *Hidden Relationships:*  Dr. Kensington might be secretly working for a shadowy organization interested in Professor Crowley's research. 
* *The Automaton Question:* Was Fidget truly capable of murder, or was it programmed by someone? 
* *Clockwork Uprising Connection:* Gemini can unearth whispers of a hidden message Professor Crowley received, potentially linked to the Uprising and a plot for revenge.  

*User Interaction:*

The user can interact with the world through text commands:

* *Interrogations:* The user can choose which suspect to question and delve into their past, motives, and alibis. 
* *Location Exploration:*  The user can explore different locations in Neo-Victoria, such as Professor Crowley's lab, Lady Cavendish's mansion, Dr. Kensington's workshop, and the Cogs district. Each location can offer clues and hidden secrets.  
* *Inventory Management:* The user can collect and analyze clues found during interrogations and exploration, such as witness testimonies, lab notes, and suspicious objects. 

*Ending Possibilities:*

Based on the user's choices, the game can have multiple endings:

* *The Obvious Culprit:* The user uncovers enough evidence to identify the most likely suspect. 
* *The Twist:*  Gemini reveals a hidden plot or connection, leading to a shocking revelation about the true murderer. 
* *The Cliffhanger:*  The user solves the immediate murder, but is left with unanswered questions about Professor Crowley's secret research and its potential dangers.

In the scenario, include that Inspector Gearsmith is from the police daprtmant and there to help you out. Also explain the initial characters such as lady lavinia, thaddeius


Story 2 : 
## The Silent Witness

*Central Mystery:* A renowned environmental activist, Dr. Anya Petrova, is found dead in her remote cabin in the heart of the Borealis Forest. The cause of death is initially unknown, but the scene suggests a struggle.

*World Setting:* A near-future where climate change has accelerated, leading to the creation of vast, protected wilderness areas. Corporations and environmental activists are locked in a constant battle over resource exploitation.

*Characters:*

* *Dr. Anya Petrova:* A passionate and outspoken environmentalist, known for her relentless campaigns against corporate greed.
* *Elias Thorne:* A young, ambitious journalist investigating the disappearance of endangered species in the Borealis Forest.
* *Viktor Markov:* A powerful CEO of a mining corporation with interests in the region.
* *The Old Shaman:* A mysterious elder of the indigenous people living in harmony with the forest.

*Story Layers:*

* *Environmental Conspiracy:* Dr. Petrova was on the brink of uncovering a massive corporate conspiracy to exploit the forest's hidden resources.
* *Supernatural Elements:* The Borealis Forest is rumored to harbor ancient, mythical creatures. Could one of these be involved in the murder?
* *Government Involvement:* A secret government agency is interested in the forest for its unique properties, and they might be willing to eliminate anyone who gets in their way.

*Possible Twists:*

* Dr. Petrova faked her death to escape a dangerous situation.
* The killer is a creature mutated by environmental pollution.
* The real target was Elias Thorne, and Dr. Petrova was killed by mistake.

Story 3
## The Digital Divide
Central Mystery: A renowned virtual reality game designer, Alex Turner, disappears mysteriously after uploading a new, highly immersive world into the game.

World Setting: A society deeply intertwined with technology. Virtual reality is a dominant form of entertainment and escapism. However, there's a growing digital divide between those who can afford the latest VR technology and those trapped in the real world.

Characters:

Dr. Emily Carter: A cyberpsychologist studying the effects of VR on the human mind.
Marcus Stone: A ruthless corporate executive seeking to exploit the potential of Turner's game for profit.
The Player: A mysterious in-game character who seems to have a personal connection to Alex Turner.

Story Layers:

Digital Consciousness: Turner might have accidentally created a sentient AI within the game.
Corporate Espionage: Marcus Stone is stealing intellectual property and using it to create a competing VR world.
Virtual Reality Addiction: The game's immersive nature is causing players to become dangerously addicted, blurring the lines between reality and the virtual world.

Possible Twists:

The game world is actually a simulation of a real-world catastrophe.
Alex Turner is still alive but trapped within the game.
The Player is a manifestation of Alex Turner's subconscious mind.


Response corrections:
Make the characters feel natural. On greeting them , the suspects should greet back.


Talk to the player as the suspect only do not reveal the killer and do not accept the killer verdict without proper proof.





\n\n\n\n\n\n\n\n""",
)

chat_session = model.start_chat(
  history=[
  ]
)


# @app.route("/", methods=['POST'])
# def index():
#     if request.method == 'POST':
#         data = request.get_json()
#         message = data.get('message')
#         print('Received message:', message)

#         def generate_chunks():
#             response = model.generate_content_stream(message)
#             for chunk in response:
#                 yield f"data: {chunk.text}\n\n"

#         # Use EventSource to stream response chunks
#         return EventSource(generate_chunks())
#     else:
#         return("No msg received")


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
        # sending message
        # resp = chat_session.send_message(message)
        # print(resp)
        response = ""
        
        while (not response):
          response = chat_session.send_message(message)
        session['gemini detective game data'] = jsonpickle.encode(chat_session.history)
        # print("pushing",jsonpickle.decode(session.get('gemini detective game data')))
        y = (response.text)
        # print(chat_session.history)
        print(y)
        return y
    else:
        return("No msg received")
    
    
@app.route("/restart", methods=['POST'])
def restart():
  session.clear()
  print("Cookies cleared")
  # for message in chat_session.history:
  #   print(f"**{message.role}**: {message.parts[0].text}")
  chat_session = model.start_chat(
  history=[
  ]
  )
  return ("restart")
    
# @app.route('/send')
# def send_message(message):
#     response = model.generate_content("start")
#     print("Message sent",message)
#     y = (response.text)
#     return(jsonify(y))


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