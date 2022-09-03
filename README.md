# Python-Google-Text-To-Speech-Jarvis-AI-Speech-Recognition-Alexa-Replacement


## Synopsis

Many thanks to a lovely guy, who inspired me to learn some python. 
Watch his tutorial, where he makes the original project "Romantic Alexa" [right in front of your eyes](https://www.youtube.com/watch?v=AWvsXxDtEkU)
I just made some cosmetical changes to it and swapped the funky python voice lib with something more pleasant from Google.

This will be a part of the pet project I'm working on - [to build an ultimate entertainment / desktop replacement machine out of cheap ARM SBC](https://orange-pi-4-lts.blogspot.com/p/todo.html). So this "voice assistant" will be running as background daemon with the system startup.

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

4. Make sure you have /usr/local/bin in your $PATH, if not - change the profile

5. Create a service, that will be executed for multi-user.target (look inside .service file, you might need to update your path)


```
sudo cp $(pwd)/voiceassistant.service /lib/systemd/system/voiceassistant.service 
sudo systemctl daemon-reload 
sudo systemctl enable voiceassistant.service 
sudo systemctl start voiceassistant.service 
sudo systemctl status voiceassistant.service
```

## Uninstall

```
sudo systemctl stop voiceassistant.service
sudo systemctl disable voiceassistant.service
rm /lib/systemd/system/voiceassistant.service 
systemctl daemon-reload
```

This step doesn't work yet. Run  it manually:
python3 main.py

## TODO:

0. Fix bug with service
  - where the heck is log written to?
  - hearing doesn't work
  - playback doesn't work
  
1. Multi-language support
   https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang
   https://pypi.org/project/SpeechRecognition/
   
2. Query DuckDuckGo by default
   https://duckduckgo.com/api
   https://pypi.org/project/DuckDuckGo-Python3-Library/
   https://github.com/crazedpsyc/python-duckduckgo/

3. Cache mp3 files to /tmp in "sayit"

4. Dialog mode, as an alternative to wake-up word:
    - hey orange
    - yeah?
    - what is the best search engine?
    - (no applicable command found => get answer from DDG)

5. Switch from online recognition to Mozilla Deep Speech

6. Implement a fallback mechanism in sayit shell file, so if internet is not around (and gTTS won't work) we'll switch to something different 

7. Implement some more commands, like "Switch to gaming mode" / "Enough of gaming" with confirmations

8. Return the browser manipulation tool back (DISPLAY issue, when X is not started)
