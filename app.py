from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import base64
import sys

from src.pipeline.run_meme_generator_pipeline import run_pipeline, fetch_image_templates
from src.exceptions import CustomException

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class TopicInput(BaseModel):
    topic_name: str

# --- Routes ---

@app.post("/generate-meme", summary="Generate meme and return PNG")
def generate_meme_api(input: TopicInput):
    try:
        result = run_pipeline(input.topic_name)
        image_bytes = result["image_bytes"]
        emotion = result["emotion"]

        image_bytes.seek(0)

        return StreamingResponse(
            image_bytes,
            media_type="image/png",
            headers={"X-Emotion": emotion}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-meme-base64", summary="Generate meme and return as base64")
def generate_meme_base64_api(input: TopicInput):
    try:
        result = run_pipeline(input.topic_name)
        image_bytes = result["image_bytes"]
        emotion = result["emotion"]

        image_bytes.seek(0)
        base64_str = base64.b64encode(image_bytes.read()).decode()

        return {
            "status": "success",
            "emotion": emotion,
            "image_base64": f"data:image/png;base64,{base64_str}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fetch-templates", summary="Fetch image templates from Supabase")
def fetch_templates_api():
    try:
        result = fetch_image_templates()
        return JSONResponse(content={"status": "success", "templates": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
