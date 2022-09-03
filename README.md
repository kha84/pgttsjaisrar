# Python-Google-Text-To-Speech-Jarvis-AI-Speech-Recognition-Alexa-Replacement


## Synopsis

Many thanks to a lovely guy, who inspired me to learn some python. 
Watch his tutorial, where he makes the original project "Romantic Alexa" [right in front of your eyes](https://www.youtube.com/watch?v=AWvsXxDtEkU)
I just made some cosmetical changes to it and swapped the funky python voice lib with something more pleasant from Google.

This will be a part of the pet project I'm working on - [to build an ultimate entertainment / desktop replacement machine out of cheap ARM SBC](https://orange-pi-4-lts.blogspot.com/p/todo.html). So this "voice assistant" will be running as background daemon with the system startup.

But it doesn't mean you need to have the same device as me - it could run on any Linux machine. 

## Demo

[![Watch the demo](https://img.youtube.com/vi/STfxY-XwTko/0.jpg)](https://www.youtube.com/watch?v=STfxY-XwTko "Voice assistant for SBC")

## Installation (Debian Bullseye 11)


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

This script can be used alone in commandline as a simple text-to-speech wrapper. 
It will get a very simple fallback option soon, so if it detects there's an issue with gTTS (or with your internet) it will switch to [something different like espeak or festival](https://orange-pi-4-lts.blogspot.com/2022/09/speech-recognition-and-text-to-speech.html). 
So far, just make sure you have /usr/local/bin in your $PATH. 
If you don't modify your profile scripts ~/.profile or ~/.bashrc to add it

4. Test the voice assistant by running it stand alone:

```
python3 main.py
```

Give it 10 or so seconds to warm up, look after logs it's printing and then say out loud "Orange, who is Donald Trump?"

5. Create a systemd service, that will be executed for multi-user.target.
Before doing that, look inside voiceassistant.service file. 
You might need to update the path to main.py script, as you installed it to different than mine location.
Also make sure that xxx in "User=xxx" there is actually the user, who is running PulseAudio process. To get that to know run 
```
ps -ef | grep -i pulseaudio
```
In my case PulseAudio server is running under **pi**, so this service will be also runing under pi

Install the service:
```
sudo cp ./voiceassistant.service /lib/systemd/system/voiceassistant.service 
sudo systemctl daemon-reload 
sudo systemctl enable voiceassistant.service 
sudo systemctl start voiceassistant.service 
sudo systemctl status voiceassistant.service
```

## Uninstall instructions

```
sudo systemctl stop voiceassistant.service
sudo systemctl disable voiceassistant.service
rm /lib/systemd/system/voiceassistant.service 
systemctl daemon-reload
rm /usr/local/bin/sayit
```

## Usage notes / troubleshooting

### Make sure to visit main.py to see what commands are there

Given I have a very specific use case for my project, I do have an EmulationStation started in multi-user.target. 
You will definitely want to change/delete couple of commands in **main.py**. 
The code is very simple and fun to play with, thanks to the original creator. 

Whenever you change anything in main.py, make sure to restart the service so your changes will start to take effect:
```
systemctl restart voiceassistant.service
```

### Where to see logs

When the voice assistant is installed as service, logs will be collected by journald. 
You can see them like this:
```
journalctl -f -u voiceassistant.service
```

If you started the assistant from the command line, logs will be printed right to stdout as usual.

### Audio issues

I only tested this script on my Orange PI 4 LTS which is having a built-in microphone.
pyAudio / SpeechRecognition puthon packages did a great job detecting it and using it as the default input device. But you might be less lucky than me.

If you have any microphone troubles, make sure your mic is detected by pyAudio / SpeechRecognition, by running the main.py as stand-alone (not as deamon). It prints a lot
of stuff at the begining which is related to audio devices detection by pyAudio. Troubleshoot that as a generic issue.

If the script dosn't play anything as a response to your questions, make sure you can run shell **sayit** script under the non-privileged user and you hear the sound:
```
/usr/local/bin/sayit "This is the voice of Google. Testing, testing, one, two, three"
```

Also make sure you can run it with using sudo, but under the same user, who's owning PulseAudio (in my case it's **pi**):

```
# first become a root to clean env
sudo su -
# then attempt to run sayit, but under your original user (mine was pi)
sudo -u pi sayit "Say it again"
```
I had to export XDG_RUNTIME_DIR in sayit, otherwise all audio playback tools using PulseAudio didn't know which one to use. 


## Project TODO
  
1. Multi-language support
   https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang
   https://pypi.org/project/SpeechRecognition/
   
3. Cache mp3 files to /tmp in "sayit" to avoid extra network hops to google text-to-speech

4. Dialog mode, as an alternative to wake-up word:
    - hey orange
    - yeah?
    - what is the best search engine?
    - (no applicable command found => get answer from DDG)

5. Switch from online recognition to Mozilla Deep Speech or similar

6. Implement a fallback mechanism in sayit shell file, so if internet is not around (and gTTS won't work) we'll switch to something different 

7. Implement confirmations for dangerous commands  like "Switch to gaming mode" / "Enough of gaming" / "Reboot"

8. Restructure the code a bit:
    - so it won't be just silly plaintext matching, but using regexp 
    - add to the same place of config bindings to various functions to call, so it won't be that scattered among the code

9. Return the browser manipulation tool back (DISPLAY issue, when X is not started in multi-user.target)
