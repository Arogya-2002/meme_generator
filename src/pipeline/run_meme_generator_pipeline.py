from src.exceptions import CustomException
from src.logger import logging
from src.components.topic_ingestion import TopicIngestion
from src.components.emotion_analyzer import EmotionAnalyzer
from src.components.memes_generator import MemesGenerator
from src.utils.image_templates import MemeTemplates
from io import BytesIO

import sys

def ingest_topic(topic_name: str):
    try:
        topic_ingestion = TopicIngestion()
        artifact = topic_ingestion.initiate_topic_ingestion(topic_name)
        return artifact.topic_name
    except Exception as e:
        raise CustomException(e, sys)

def analyze_emotion(text: str):
    try:
        emotion_analyzer = EmotionAnalyzer()
        return emotion_analyzer.analyze_emotion(text)
    except Exception as e:
        raise CustomException(e, sys)

def fetch_image_templates():
    try:
        meme_temp = MemeTemplates()
        meme_temp.get_emotion_images()
        return {"status": "success", "message": "Templates fetched successfully"}
    except Exception as e:
        raise CustomException(e, sys)

def generate_meme(topic_name: str, emotion: str) -> BytesIO:
    try:
        memes_generator = MemesGenerator()
        image_bytes = memes_generator.initiate_meme_generator(topic_name, emotion)
        return image_bytes
    except Exception as e:
        raise CustomException(e, sys)


def run_pipeline(topic_name: str):
    try:
        text = ingest_topic(topic_name)
        emotion_artifact = analyze_emotion(text)
        image_bytes = generate_meme(topic_name, emotion_artifact.emotion_name)

        return {
            "image_bytes": image_bytes,
            "emotion": emotion_artifact.emotion_name
        }
    except Exception as e:
        raise CustomException(e, sys)
    
if __name__ == "__main__":
    try:
        topic_name = "exam failed"  # Replace with your topic name
        result = run_pipeline(topic_name)
        print(f"Generated meme for emotion: {result['emotion']}")
    except CustomException as e:
        logging.error(f"Pipeline failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")