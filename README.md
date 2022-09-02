# Python-Google-Text-To-Speech-Jarvis-AI-Speech-Recognition-Alexa-Replacement


## Synopsis

Many thanks to a lovely guy, who inspired me to learn some python. 
Watch his tutorial, where he makes the original project "Romantic Alexa" (right in front of your eyes)[https://www.youtube.com/watch?v=AWvsXxDtEkU]
I just made some cosmetical changes to it and swapped the funky python voice lib with something more pleasant from Google.

This will be a part of the pet project I'm working on - (to build an ultimate entertainment / desktop replacement machine out of cheap ARM SBC)[https://orange-pi-4-lts.blogspot.com/p/todo.html]

## Installation on Debian Linux


1. Install all dependancies

```
apt install python3-tk python3-dev sox libsox-fmt-all
pip3 install gTTS speechRecognition pyttsx3 pywhatkit wikipedia pyAudio pyjokes

```

2. Clone this project to a folder of your choice

```
git clone https://github.com/kha84/pgttsjaisrar
cd pgttsjaisrar
```

3. Copy (or symlink) "sayit" script to /usr/local/bin/sayit

```
ln -s $(pwd)/sayit /usr/local/bin/sayit
```

4. Create a service, that will be executed for multi-user.target

```
TODO
```
