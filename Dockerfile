FROM python:3.9.16-bullseye
RUN apt-get update && apt-get install -y ffmpeg  espeak-ng
RUN cd / && git clone https://github.com/jasonppy/VoiceCraft.git
WORKDIR /VoiceCraft
RUN wget https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-english_mfa-v3.0.0/english_mfa.zip
RUN wget https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-english_us_arpa-v3.0.0/english_us_arpa.zip
RUN wget https://github.com/MontrealCorpusTools/mfa-models/releases/download/dictionary-english_us_arpa-v3.0.0/english_us_arpa.dict
RUN unzip english_mfa.zip
RUN unzip english_us_arpa.zip
RUN wget https://huggingface.co/pyp1/VoiceCraft/resolve/main/encodec_4cb2048_giga.th?download=true -O encodec_4cb2048_giga.th
RUN wget https://huggingface.co/pyp1/VoiceCraft/resolve/main/giga330M.pth?download=true -O giga330M.pth
RUN wget https://huggingface.co/pyp1/VoiceCraft/resolve/main/giga830M.pth?download=true -O giga830M.pth
ADD requirements-frozen.txt /VoiceCraft
RUN pip install -r /VoiceCraft/requirements-frozen.txt
RUN pip install -e git+https://github.com/facebookresearch/audiocraft.git@c5157b5bf14bf83449c17ea1eeb66c19fb4bc7f0#egg=audiocraft
RUN pip install faster-whisper==0.10.1
ADD download_models.py /VoiceCraft
RUN python3 /VoiceCraft/download_models.py
ADD app.py /VoiceCraft

ENTRYPOINT [ "python3","app.py" ]