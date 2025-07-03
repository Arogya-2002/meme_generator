import os
import sys
import google.generativeai as genai
import io

from src.exceptions import CustomException
from src.logger import logging
from src.entity.config_entity import ConfigEntity, EmotionAnalyzerConfigEntity
from src.entity.artifact_entity import EmotionAnalyzerArtifact


class EmotionAnalyzer:
    def __init__(self):
        try:
            self.emotion_analyzer_config = EmotionAnalyzerConfigEntity(config_entity=ConfigEntity())
            genai.configure(api_key=self.emotion_analyzer_config.gemini_api_key)
            self.model = genai.GenerativeModel(self.emotion_analyzer_config.gemini_model_name)
        except Exception as e:
            raise CustomException(e, sys)

    def analyze_emotion(self, text: str) -> EmotionAnalyzerArtifact:
        try:
            logging.info("Analyzing emotion in text...")

            prompt = (
                "Categorize the emotional tone of the following text into one of the following categories:\n"
                "happy, sad, angry, surprise, neutral, sarcastic.\n"
                f"Text: {text}\n"
                "Return ONLY the emotion as a single word."
            )

            response = self.model.generate_content(prompt)
            emotion = getattr(response, "text", "").strip().lower()

            if not emotion:
                raise ValueError("Gemini returned an empty response.")

            if emotion not in self.emotion_analyzer_config.emotion_templates:
                emotion = "neutral"

            logging.info(f"Emotion analyzed: {emotion}")
            return EmotionAnalyzerArtifact(emotion_name=emotion)

        except Exception as e:
            raise CustomException(e, sys)


# Optional: only run this for direct script testing
# if __name__ == "__main__":
#     try:
#         emotion_analyzer = EmotionAnalyzer()
#         text = "I failed my exam today."
#         artifact = emotion_analyzer.analyze_emotion(text)
#         print(f"Analyzed Emotion: {artifact}")
#     except Exception as e:
#         logging.error(f"Error in emotion analysis: {e}")
#         raise CustomException(e, sys)
