# Disclaimer from the Voicecraft Github repo
Any organization or individual is prohibited from using any technology mentioned in this paper to generate or edit someone's speech without his/her consent, including but not limited to government leaders, political figures, and celebrities. If you do not comply with this item, you could be in violation of copyright laws.

# Description
A dockerized version of VoiceCraft [CUDA only] offering a gradio interface [voicecraft github](https://github.com/jasonppy/VoiceCraft/) and inspired by this [webio](https://github.com/Pathos14489/VoiceCraft/blob/master/webio.py) implementation.
```sh
# docker build -t voicecrafter
# docker run --gpus=all -p 7860:7860 -it voicecrafter
```

# Screenshot
<img width="1313" alt="image" src="https://github.com/pselvana/VoiceCrafter/assets/1414489/831bcf0e-4682-454c-8f8c-18462f4b328a">


# Instructions
- Run the above to start your instance
- Visit the gradio.live or the local link (note: not currently authenticated so anyone with the link can use it)
- Click the "Original Audio" tile to upload clear audio of only the subject speaking on the order of 5-10 seconds. Trim out anything longer and choose audio with no background noise or crackles and pops (file formats: mp3, m4a, wav)
- Update the "original_transcript" with the transcript of the audio uploaded or leave the Autotranscribe input checkbox checked
- Update "target_transcript" with the sentence or two of text you want to generate
- Click "Run" to generate audio
- Click the play button next to "Generated Audio" to hear the clip and the "..." to download

# Models
| Model    | Parameters | Memory | Runs on |
| -------- | ------- | ------- | ------- |
| fast-whisper  |   |   | CPU |
| voicecraft | 330M     | 4GB+ VRAM | GPU |
| voicecraft    | 830M    | 6GB+ VRAM | GPU |


# Original VoiceCraft License
The codebase is under CC BY-NC-SA 4.0 (LICENSE-CODE), and the model weights are under Coqui Public Model License 1.0.0 (LICENSE-MODEL). Note that we use some of the code from other repository that are under different licenses: ./models/codebooks_patterns.py is under MIT license; ./models/modules, ./steps/optim.py, data/tokenizer.py are under Apache License, Version 2.0; the phonemizer we used is under GNU 3.0 License.

Please refer to the below for latest:
- [LICENSE-CODE](https://github.com/jasonppy/VoiceCraft/blob/master/LICENSE-CODE)
- [LICENSE-MODEL](https://github.com/jasonppy/VoiceCraft/blob/master/LICENSE-MODEL)
