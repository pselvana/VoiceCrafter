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
from models import voicecraft


os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   
os.environ["CUDA_VISIBLE_DEVICES"]="0" 
os.environ["USER"] = "root"

encodec_fn = "./encodec_4cb2048_giga.th"
device = "cuda" if torch.cuda.is_available() else "cpu"

current_model = None
model = None
ckpt = None

#load tokenizers
from data.tokenizer import (
    AudioTokenizer,
    TextTokenizer,
)
text_tokenizer = TextTokenizer(backend="espeak")
audio_tokenizer = AudioTokenizer(signature=encodec_fn) # will also put the neural codec model on gpu

# run the model to get the output

from inference_tts_scale import inference_one_sample

def tts(original_audio, original_transcript, target_transcript, top_k=0, top_p=0.8, temperature=1, stop_repetition=3,inverse_offset=0, model_weight="830M"):
    global current_model
    global model
    global ckpt

    if current_model == None or current_model != f"./giga"+model_weight+".pth":
        ckpt_fn =f"./giga"+model_weight+".pth"
        ckpt = torch.load(ckpt_fn, map_location="cpu")

        model = voicecraft.VoiceCraft(ckpt["config"])
        model.load_state_dict(ckpt["model"])
        model.to(device)
        model.eval()
        current_model=ckpt_fn
        print ("Loaded and using: "+current_model)


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

input_audio = gr.Audio(label="Original Audio", type="filepath")
output_audio = gr.Audio(label="Generated Audio", type="filepath")

original_transcript_input = gr.Textbox(label="Uploaded Audio Transcript")
new_transcript_input = gr.Textbox(label="What would you like to say?")
top_k_input = gr.Number(label="Top K", value=0)
top_p_input = gr.Number(label="Top P", value=0.8)
temperature_input = gr.Number(label="Temperature", value=1)
stop_word_count_input = gr.Number(label="Stop Word Count", value=3)
inverse_offset_input = gr.Number(label="Inverse Offset", value=0)
model_input = gr.Radio(label="Select Option", choices=["330M", "830M"])

iface = gr.Interface(fn=tts, inputs=[input_audio, original_transcript_input, new_transcript_input, top_k_input, top_p_input, temperature_input, stop_word_count_input, inverse_offset_input, model_input], outputs=output_audio)

iface.launch(share=True)