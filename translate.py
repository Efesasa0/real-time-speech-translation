from os import system
import sys
import pyaudio
import threading
import queue
import time
import datetime

from audio_op import find_device_id, record_audio
from prep_model import prep, run

def get_time():
    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    human_readable = dt_object.strftime('%H:%M:%S')
    return human_readable

def listener(audio, device_id, lq):
    while True:
        audio_data = record_audio(audio, device_id)
        lq.put(audio_data)
        #print(f"@@ added{get_time()}")

def transcriber(model, lq, sq, task="translate"):
    while True:
        audio_data_bytes, channels, sample_width, rate = lq.get()
        _, _, audio_text = run(model=model,
                               task=task,
                               audio_data_bytes=audio_data_bytes,
                               channels=channels,
                               sample_width=sample_width,
                               frame_rate=rate
                               )
        sq.put(audio_text)
        #print(f"processed{get_time()}")
        print(audio_text)

def speaker(sq):
    while True:
        audio_text = sq.get()
        system(f'say {audio_text}')
        print(sq)

def main():
    if len(sys.argv) != 2:
        print("Usage: python den04.py device_name")
        sys.exit(-1)
    device_name = sys.argv[1]

    audio = pyaudio.PyAudio()
    audio, device_id = find_device_id(audio, device_name)
    model = prep("base")

    listen_q = queue.Queue()
    speech_q = queue.Queue()

    producer_thread = threading.Thread(target=listener, args=(audio, device_id, listen_q,))
    consumer_thread = threading.Thread(target=transcriber, args=(model, listen_q, speech_q,))
    speaker_thread = threading.Thread(target=speaker, args=(speech_q,))

    producer_thread.start()
    consumer_thread.start()
    speaker_thread.start()

    producer_thread.join()
    consumer_thread.join()
    speaker_thread.join()

    audio.terminate()
    print("All threads have been terminated.")

if __name__ == "__main__":
    main()