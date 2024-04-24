# Real-Time Speech Translation

## Overview
The project attempts to record live audio from an **input device** of choice and translates the speech to english with [faster_whisper](https://github.com/SYSTRAN/faster-whisper) by SYSTRAN.

For **Mac** users, to capture internal audio, (BlackHole)[https://existential.audio/blackhole/] by Existential Audio setup is recommended. [Further info will be discussed down...](#BlackHole_Setup)

## Features
* Real-time audio capture from specified audio device.
* Real-time audio transcription/translation
* Real-time feedback of transcription/translation with Text to Speech (mac only)

## Setup/Installation and Run
```bash
git clone https://github.com/Efesasa0/real-time-speech-translation.git
cd real-time-speech-translation
```
Basically Install faster_whisper, py_audio, torch and wave.

```bash
pip install -r requirements.txt
```

To run, enter the current input device name for your machine in quotes. (may need to change the input device on your machine manually)
```bash
python translate.py "<your device name here>"
```

As of now, control+C is the only way to quit 😬. Not gracefull I know...

<h1 id="BlackHole_Setup">BlackHole setup</h1>

### Mac Solution

1. Go to https://existential.audio/blackhole/ and download BlackHole (preferably 2ch version)
2. set input device to blackhole from MIDI app.
3. create **Multi-Output Device**
4. In it select Blachole and the your headphones or speakers then give the **Multi-Output Device** a new name.
5. set that Device as your output source device.
6. Choose 48000 Hz or 44100 Hz for BlackHole and your Multi-Output Device. make sure choose one for all.
7. Use "BlackHole 2ch" when running.

## Limitations 👎:
1. is fuzzy translation due to the nature of the problem.
2. not so gracegull termination as of now.
3. tts needs revision.
## Ups 👍:
1. Optimized for efficient memory use!

# Some Resources
1. https://github.com/ggerganov/whisper.cpp
2. https://github.com/openai/whisper
3. https://github.com/SYSTRAN/faster-whisper
4. https://existential.audio/blackhole/
