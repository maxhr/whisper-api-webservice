# docker run --gpus all -p 9000:80 -p 80:9000 -e ASR_MODEL=large-v2 -e ASR_ENGINE=faster_whisper -v /whisper-cache:/root/.cache/whisper -v /faster_whisper-cache:/root/.cache/faster_whisper onerahmet/openai-whisper-asr-webservice:latest-gpu

# git clone https://github.com/maxhr/whisper-api-webservice.git
# cd whisper-api-webservice
# chmod +x ./run.sh
# ./run.sh

sudo docker build -f Dockerfile-whisper-gpu -t whisper-jax .
sudo docker run -d --gpus all --network=host -e TF_CPP_MIN_LOG_LEVEL=0  -v /jax-cache:/jax-cache -v /huggingface-cache:/root/.cache/huggingface/hub whisper-jax
sudo docker build -f Dockerfile -t whisper-api .
sudo docker run -d --network=host whisper-api
