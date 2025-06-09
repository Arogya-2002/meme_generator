from src.exceptions import CustomException
from src.logger import logging
from src.constants import *

import sys

class ConfigEntity:
    def __init__(self):
        self.template_dir = TEMPLATE_DIR
        self.font_path = FONT_PATH
        self.gemini_api_key = API_KEY
        self.model_name = MODEL_NAME
        self.topic_name = TOPIC_NAME
        self.emotion_templates = EMOTION_TEMPLATES
        self.supabase_url = SUPABASE_URL
        self.supabase_key = SUPABASE_KEY
        self.bucket_path = BUCKET_PATH
        self.template_dir = TEMPLATES_DIR
        self.json_file = JSON_FILE
        self.output_dir = OUTPUT_DIR
        self.memes_dir = MEMES

class TopicIngestionConfigEntity:
    def __init__(self, config_entity: ConfigEntity):  # ← FIXED: __init__
        self.topic_name = config_entity.topic_name



class EmotionAnalyzerConfigEntity:
    def __init__(self, config_entity: ConfigEntity):
        self.gemini_model_name = config_entity.model_name
        self.gemini_api_key = config_entity.gemini_api_key
        self.emotion_templates = config_entity.emotion_templates

class MemeTemplatesEntity:
    def __init__(self, config_entity: ConfigEntity):
        self.supabase_url = config_entity.supabase_url
        self.supabase_key = config_entity.supabase_key
        self.bucket_path = config_entity.bucket_path
        self.template_dir = config_entity.template_dir
        self.font_path = config_entity.font_path
        self.json_file = config_entity.json_file
        self.output_dir = config_entity.output_dir
        self.memes_dir = config_entity.memes_dir
