import os
from fastapi import FastAPI, File, UploadFile, APIRouter
from gradio_client import Client
import logging
import uuid

API_URL = os.environ.get("API_URL", "http://localhost:7860/")
VIDEO_DIRECTORY = "static"
os.makedirs(VIDEO_DIRECTORY, exist_ok=True)

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("whisper")

app = FastAPI()
router = APIRouter()
# client = Client(API_URL)

def transcribe_audio(audio_path, task="transcribe", return_timestamps=False):
    client = Client(API_URL)
    text, runtime = client.predict(
        audio_path,
        task,
        return_timestamps,
        api_name="/predict_1",
    )
    return text

@router.get("/")
async def home():
    return {"message": "OK"}

@router.post("/asr")
async def asr(audio_file: UploadFile = File(...)):
    filepath = os.path.basename(audio_file.filename)
    logger.info(filepath)

    audio_path = f"{VIDEO_DIRECTORY}/{str(uuid.uuid4())}"
    with open(audio_path, "wb+") as fp:
        fp.write(audio_file.file.read())

    try:
        output_with_timestamps = transcribe_audio(audio_path, return_timestamps=False)
        return output_with_timestamps
    except Exception as e:
        raise RuntimeError(f"Error: {e}") from e
    finally:
        os.remove(audio_path)

app.include_router(router)

# if __name__ == "__main__":
#     uvicorn.run("app:app", reload=True, port=6000, host="0.0.0.0")
