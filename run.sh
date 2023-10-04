docker run --gpus all -p 9000:80 -p 80:9000 -e ASR_MODEL=large-v2 -e ASR_ENGINE=faster_whisper -v /whisper-cache:/root/.cache/whisper -v /faster_whisper-cache:/root/.cache/faster_whisper onerahmet/openai-whisper-asr-webservice:latest-gpu

docker run -p 7890:7890 Dockerfile

sudo docker build -f Dockerfile -t whisper .
sudo docker run  --privileged --network=host  -v /jax-cache:/jax-cache -v /huggingface-cache:/root/.cache/huggingface/hub whisper



docker build -f Dockerfile -t whisper . && docker run  -p 8080:8080 whisper
