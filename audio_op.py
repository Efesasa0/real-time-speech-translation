import pyaudio
from io import BytesIO

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000 #48000 #44100
CHUNK = 1024
RECORD_SECONDS = 5

def find_device_id(audio, device_name):
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for device_id in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, device_id).get('maxInputChannels')) > 0:
            if device_name == audio.get_device_info_by_host_api_device_index(0, device_id).get('name'):
                return audio, device_id
    raise ValueError(f"Device named {device_name} cannot be found.")

def record_audio(audio, device_id):
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=device_id,
                        frames_per_buffer=CHUNK)
    
    device_name = audio.get_device_info_by_host_api_device_index(0, device_id).get('name')
    #print(f"Recording from {device_name} for {RECORD_SECONDS} seconds")
    audio_data = BytesIO()

    for _ in range(int(RATE/CHUNK*RECORD_SECONDS)):
        data = stream.read(CHUNK)
        audio_data.write(data)
    #print("Finished Recording")
    stream.stop_stream()
    stream.close()
    audio_data.seek(0)
    return audio_data.read(), CHANNELS, 2, RATE

def play_audio(audio, audio_data):
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True)
    audio_data_chunk = audio_data.read(CHUNK)

    while audio_data_chunk:
        stream.write(audio_data_chunk)
        audio_data_chunk = audio_data.read(CHUNK)

    stream.stop_stream()
    stream.close()