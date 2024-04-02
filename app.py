import os
from phonemizer.backend.espeak.wrapper import EspeakWrapper
#_ESPEAK_LIBRARY = 'C:\Program Files\eSpeak NG\libespeak-ng.dll'
#EspeakWrapper.set_library(_ESPEAK_LIBRARY)
# import libs
import torch
import torchaudio
import gradio as gr
import os

from pydub import AudioSegment

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   
os.environ["CUDA_VISIBLE_DEVICES"]="0" 
os.environ["USER"] = "root"

ckpt_fn =f"./giga330M.pth"
encodec_fn = "./encodec_4cb2048_giga.th"

ckpt = torch.load(ckpt_fn, map_location="cpu")
device = "cuda" if torch.cuda.is_available() else "cpu"

from models import voicecraft
model = voicecraft.VoiceCraft(ckpt["config"])
model.load_state_dict(ckpt["model"])
model.to(device)
model.eval()

from data.tokenizer import (
    AudioTokenizer,
    TextTokenizer,
)
text_tokenizer = TextTokenizer(backend="espeak")
audio_tokenizer = AudioTokenizer(signature=encodec_fn) # will also put the neural codec model on gpu

# run the model to get the output

from inference_tts_scale import inference_one_sample

def tts(original_audio, original_transcript, target_transcript, top_k=0, top_p=0.8, temperature=1, stop_repetition=3,inverse_offset=0):
    decode_config = {
        'top_k': top_k,
        'top_p': top_p,
        'temperature': temperature,
        'stop_repetition': stop_repetition, # if there are long silence in the generated audio, reduce the stop_repetition to 3, 2 or even 1
        'kvcache': 1,
        "codec_audio_sr": 16000,
        "codec_sr": 50,
        "silence_tokens": [1388,1898,131],
        "sample_batch_size": 3 # if there are long silence or unnaturally strecthed words, increase sample_batch_size to 2, 3 or even 4
    }

    print(original_audio)
    converted_audio = "/tmp/input.wav"

    sound = AudioSegment.from_mp3(original_audio)
    sound.export(converted_audio, format="wav")


    target_transcript = original_transcript + target_transcript
    info = torchaudio.info(converted_audio)
    cut_off_sec = info.num_frames / info.sample_rate
    audio_dur = info.num_frames / info.sample_rate
    assert cut_off_sec <= audio_dur, f"cut_off_sec {cut_off_sec} is larger than the audio duration {audio_dur}"
    prompt_end_frame = int(cut_off_sec * info.sample_rate) - int(inverse_offset)
    print(f"prompt_end_frame:",prompt_end_frame)
    _, gen_audio = inference_one_sample(model, ckpt["config"], ckpt['phn2num'], text_tokenizer, audio_tokenizer, converted_audio, target_transcript, device, decode_config, prompt_end_frame)
    gen_audio = gen_audio[0].cpu()
    torchaudio.save(f"gen.wav", gen_audio, 16000)
    return "gen.wav"

input_audio = gr.inputs.Audio(label="Original Audio", type="filepath")
output_audio = gr.outputs.Audio(label="Generated Audio", type="filepath")

iface = gr.Interface(fn=tts, inputs=[input_audio, "text", "text", "number", "number", "number", "number", "number"], outputs=output_audio)

iface.launch(share=True)