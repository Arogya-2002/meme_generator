from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from io import BytesIO
from uvicorn import run as uvicorn_run

from src.exceptions import CustomException
from src.logger import logging
from src.pipeline.run_meme_generator_pipeline import run_pipeline, fetch_image_templates  # Assuming your code is in pipeline.py

app = FastAPI(title="Meme Generator API with Emotion Analysis")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class TopicRequest(BaseModel):
    topic_name: str

@app.get("/")
def root():
    return {"message": "Welcome to the Meme Generator API!"}


@app.post("/generate-meme/")
def generate_meme_api(request: TopicRequest):
    try:
        result = run_pipeline(request.topic_name)

        # Move pointer to start of BytesIO stream
        result["image_bytes"].seek(0)

        return StreamingResponse(
            result["image_bytes"],  # Pass the BytesIO object directly
            media_type="image/png",
            headers={"X-Emotion": result["emotion"]}
        )
    except CustomException as e:
        logging.error(f"CustomException: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/fetch-templates/")
def fetch_templates_api():
    try:
        response = fetch_image_templates()
        return response
    except CustomException as e:
        logging.error(f"Template fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn_run("app:app",host="0.0.0.0", port=8000, reload=True)