import speech_recognition as sr
import pyttsx3
#import pywhatkit
import datetime
import wikipedia
import pyjokes
import subprocess

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk_orig(text):
    engine.say(text)
    engine.runAndWait()


def talk(text):
    if not text:
        print("Warning: no text was given to talk function")
        return 
    print("Talking this text: "+text)
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
            if 'orange' in command:
                command = command.replace('orange', '')
                print('Got command: '+command)
                return command
    except:
        return ''
    return ''


def run_alexa():
    command = take_command()
    print("run_alexa() got command: " + command)
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
        print(info)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'stop listening' in command:
        talk("Bye-bye!")
        quit()
    else:
        talk("Sorry did't get it")

while True:
    run_alexa()
