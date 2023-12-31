from __future__ import annotations
import functools
import os
from transformers import pipeline
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, APIRouter
from gradio_client import Client
import logging
import uuid
from faster_whisper import WhisperModel
from whisper_jax import FlaxWhisperPipline
import jax.numpy as jnp
import whispercpp

# API_URL = os.environ.get("API_URL", "http://localhost:7860/")
VIDEO_DIRECTORY = "static"
os.makedirs(VIDEO_DIRECTORY, exist_ok=True)

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("whisper")

# faster_whisper_model = WhisperModel("large-v2", device="cuda", compute_type="float16")
# pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v2", device="cuda")
# jax_pipe = FlaxWhisperPipline("openai/whisper-large-v2", dtype=jnp.float16)

app = FastAPI()
router = APIRouter()
# client = Client(API_URL)

# def transcribe_audio(audio_path, task="transcribe", return_timestamps=False):
#     client = Client(API_URL)
#     text, runtime = client.predict(
#         audio_path,
#         task,
#         return_timestamps,
#         api_name="/predict_1",
#     )
#     return text

wisper_cpp = whispercpp.Whisper.from_pretrained("large")

@router.get("/")
async def home():
    return {"message": "OK"}

@router.post("/whisper-cpp")
async def asr(audio_file: UploadFile = File(...)):
    filepath = os.path.basename(audio_file.filename)
    logger.info(filepath)

    audio_path = f"{VIDEO_DIRECTORY}/{str(uuid.uuid4())}"
    with open(audio_path, "wb+") as fp:
        fp.write(audio_file.file.read())

    converted_audio_path = f"{audio_path}-converted.wav"
    os.system(f"ffmpeg -i {audio_path} -ar 16000 -ac 1 -c:a pcm_s16le {converted_audio_path}")

    try:
        output = wisper_cpp.transcribe_from_file(converted_audio_path)
        return output
    except Exception as e:
        raise RuntimeError(f"Error: {e}") from e
    finally:
        os.remove(audio_path)
        os.remove(converted_audio_path)


@router.post("/jax")
async def asr(audio_file: UploadFile = File(...)):
    filepath = os.path.basename(audio_file.filename)
    logger.info(filepath)

    audio_path = f"{VIDEO_DIRECTORY}/{str(uuid.uuid4())}"
    with open(audio_path, "wb+") as fp:
        fp.write(audio_file.file.read())

    try:
        output = jax_pipe(audio_path)
        return output
    except Exception as e:
        raise RuntimeError(f"Error: {e}") from e
    finally:
        os.remove(audio_path)

@router.post("/whisper")
async def whisper(audio_file: UploadFile = File(...)):
    filepath = os.path.basename(audio_file.filename)
    logger.info(filepath)

    audio_path = f"{VIDEO_DIRECTORY}/{str(uuid.uuid4())}"
    with open(audio_path, "wb+") as fp:
        fp.write(audio_file.file.read())

    try:
        output = pipe(audio_path)
        return output
    except Exception as e:
        raise RuntimeError(f"Error: {e}") from e
    finally:
        os.remove(audio_path)

@router.post("/faster-whisper")
async def whisper(audio_file: UploadFile = File(...)):
    filepath = os.path.basename(audio_file.filename)
    logger.info(filepath)

    audio_path = f"{VIDEO_DIRECTORY}/{str(uuid.uuid4())}"
    with open(audio_path, "wb+") as fp:
        fp.write(audio_file.file.read())

    try:
        segments, _ = faster_whisper_model.transcribe(audio_path)
        segments = list(segments)  # The transcription will actually run here.
        return segments
    except Exception as e:
        raise RuntimeError(f"Error: {e}") from e
    finally:
        os.remove(audio_path)

app.include_router(router)

# if __name__ == "__main__":
#     uvicorn.run("app:app", reload=True, port=6000, host="0.0.0.0")
