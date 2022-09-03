import speech_recognition as sr
import pyttsx3
#import pywhatkit
import datetime
import wikipedia
import pyjokes
import subprocess
import requests
import os

## configuration ##
last_text = 'I did not say anything'
activation_word = 'orange'
phraseRepeat = ['repeat', 'say it again','pardon me']
phraseJoke = ['tell me a joke','say something funny','make me smile']
phraseExit = ['stop listening','terminate yourself','exit']
phraseAsk = ['what','who','when']
phrasePlay = ["let's play","gaming mode","enought of working"]
phraseWork = ["let's work","working mode","enought of working"]
phraseReboot=["reboot yourself","reboot computer","restart computer"]
###################

listener = sr.Recognizer()

## disabled this as we're using external shell script
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)
# 
# def talk_orig(text):
#     engine.say(text)
#     engine.runAndWait()

def ask_ddg(text):
    r = requests.get("https://api.duckduckgo.com",
        params = {
            "q": text,
            "format": "json"
        })
    data = r.json()
    if not data["Abstract"]:
        return 'I searched that in duckduckgo but it did not return me anything'
    return data["Abstract"]

def talk(text):
    if not text:
        print("Warning: no text was given to talk function")
        return 
    print("Talking this text: "+text)
    global last_text
    last_text = text;
    process = subprocess.Popen('/usr/local/bin/sayit "%s"' % str(text), shell=True)
    process.wait()
    print("Return code is: " + str(process.returncode))

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            print('transcribing...')
            command = listener.recognize_google(voice)
            print('Recognized raw: '+command)
            command = command.lower()
            if activation_word in command:
                command = command.replace(activation_word, '')
                print('Got command: '+command)
                return command
    except:
        return ''
    return ''

def run_alexa():
    command = take_command()
    if not command:
        return
#    if 'play' in command:
#        song = command.replace('play', '')
#        talk('playing ' + song)
#        pywhatkit.playonyt(song)
    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        try:
            info = wikipedia.summary(person, 1)
        except:
            info = "I have no idea"
        talk(info)
    elif any(x in command for x in phraseAsk):
        talk(ask_ddg(command))  
    elif any(x in command for x in phraseRepeat):
        talk(last_text)
    elif any(x in command for x in phraseJoke):
        talk(pyjokes.get_joke())
    ########### dangerous commands ##########
    elif any(x in command for x in phrasePlay):
        talk("Allright, let's play some games")
        # TODO: don't just blindly switch, check if the target is already there and say it if it is
        os.system('sudo systemctl isolate multi-user.target')
    elif any(x in command for x in phraseWork):
        talk("Sure, switching to working mode")
        # TODO: don't just blindly switch, check if the target is already there and say it if it is
        os.system('sudo systemctl isolate graphical.target')
    elif any(x in command for x in phraseReboot):
        talk("The machine is going to be rebooted now!")
        # TODO: ask for confirmation
        os.system('sudo reboot')
    elif any(x in command for x in phraseExit):
        talk("Bye-bye!")
        quit()
    else:
        talk("Sorry didn't get it")

while True:
    run_alexa()
