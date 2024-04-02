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
ADD requirements-frozen.txt /VoiceCraft
RUN pip install -r /VoiceCraft/requirements-frozen.txt
RUN pip install -e git+https://github.com/facebookresearch/audiocraft.git@c5157b5bf14bf83449c17ea1eeb66c19fb4bc7f0#egg=audiocraft
ADD app.py /VoiceCraft
#RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
#    /bin/bash ~/miniconda.sh -b -p /opt/conda
#RUN /opt/conda/bin/conda init --system
#RUN . /etc/profile.d/conda.sh && conda create -n voicecraft
#RUN . /etc/profile.d/conda.sh && conda activate voicecraft
#RUN /opt/conda/bin/conda install -c conda-forge montreal-forced-aligner=2.2.17 openfst=1.8.2 kaldi=5.5.1068
ENTRYPOINT [ "python3","app.py" ]