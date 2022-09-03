# Python-Google-Text-To-Speech-Jarvis-AI-Speech-Recognition-Alexa-Replacement


## Synopsis

Many thanks to a lovely guy, who inspired me to learn some python. 
Watch his tutorial, where he makes the original project "Romantic Alexa" [right in front of your eyes](https://www.youtube.com/watch?v=AWvsXxDtEkU)
I just made some cosmetical changes to it and swapped the funky python voice lib with something more pleasant from Google.

This will be a part of the pet project I'm working on - [to build an ultimate entertainment / desktop replacement machine out of cheap ARM SBC](https://orange-pi-4-lts.blogspot.com/p/todo.html). So this "voice assistant" will be running as background daemon with the system startup.

But it doesn't mean you need to have the same device as me - it could run on any Linux machine. 

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

4. Make sure you have /usr/local/bin in your $PATH, if not - change the profile

5. Test the voice assistant by running it stand alone:

```
python3 main.py
```

Give it 10 or so seconds to warm up, look after logs it's printing and then say out loud "Orange, who is Donald Trump?"

6. Create a service, that will be executed for multi-user.target.
Before doing that, look inside voiceassistant.service file. 
You might need to update the path to main.py script, if you installed it to different than mine location.
Also make sure that xxx in "User=xxx" is actually the user, who is running PulseAudio process. To get that to know run 
```
ps -ef | grep -i pulseaudio
```
In my case PulseAudio is running under pi, so the service will be also runing under pi

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

### Where to see logs

When the voice assistant is installed as service, logs will be collected by journald, and you can see them like this:
```
journalctl -x
```
... then press [SHIFT] + [F]

If you executed the assistant from the command line, logs will be printed there.

### Audio issues

I only tested it on my Orange PI 4 LTS which is having a built-in microphone.
pyAudio / SpeechRecognition puthon packages did a great job detecting it and using it as the default input device. But you might be less lucky than me.
If you have troubles with the built-in microphone or if your SBC doesn't have it, the usual suggesting would be to buy a decent USB microphone 
instead and make sure it will be detected by pyAudio / SpeechRecognition, by running it as stand-alone (not as deamon)

First make sure you can run shell **sayit** script under the non-privileged user and you hear the sound:
```
/usr/local/bin/sayit "This is the voice of Google. Testing, testing, one, two, three"
```

Also make sure you can run sayit with using sudo, but under the same user, who's owning PulseAudio (in my case it's **pi**):

```
# first become a root with clean env
sudo su -
# then attempt to run sayit under your original user
sudo -u pi sayit "Say it again"
```
I had to export XDG_RUNTIME_DIR in that script, otherwise all audio playback tools using PulseAudio didn't know which one to use. 


## Project TODO
  
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
