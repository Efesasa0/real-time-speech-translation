from faster_whisper import WhisperModel
from io import BytesIO
import torch
import wave

def prep(model_name):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = WhisperModel(model_name,
                         device=device,
                         compute_type="float32")
    return model
    
def run(model, task, audio_data_bytes, channels, sample_width, frame_rate):
    virtual_file = BytesIO()
    def create_virtual_wav(audio_data_bytes):
        with wave.open(virtual_file, "wb") as wave_file:
            wave_file.setnchannels(channels)
            wave_file.setsampwidth(sample_width)
            wave_file.setframerate(frame_rate)
            wave_file.writeframes(audio_data_bytes)
        virtual_file.seek(0)
        return virtual_file
    
    virtual_wav = create_virtual_wav(audio_data_bytes)
    segments, info = model.transcribe(audio=virtual_wav,
                                      beam_size=5,
                                      #condition_on_previous_text=False,
                                      vad_filter=True, #helps solve hallucination from empty audio
                                      task=task)
    lang = info.language
    lang_p = info.language_probability
    text = "".join(segment.text for segment in segments)
    return lang, lang_p, text