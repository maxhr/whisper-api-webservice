FROM onerahmet/openai-whisper-asr-webservice:v1.1.1

ENV ASR_MODEL=large-v2
# ENV ASR_ENGINE=openai_whisper
ENV ASR_ENGINE=faster_whisper
