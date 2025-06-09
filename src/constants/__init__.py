import os
from dotenv import load_dotenv

load_dotenv()
# Directory paths
TEMPLATE_DIR = "meme_templates"
FONT_PATH = "fonts/Noto_Sans_Telugu/NotoSansTelugu-Regular.ttf"

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


# Emotion templates
EMOTION_TEMPLATES =['happy', 'sad', 'angry', 'surprise', 'neutral', 'sarcastic']


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_PATH= os.getenv("BUCKET_PATH") 


EMOTIONS_CSV_PATH = "emotions_rows.csv"  
# Emotion templates mapping

TOPIC_NAME = None

OUTPUT_DIR = "artifacts"
TEMPLATES_DIR = "template_dir"
JSON_FILE = "emotion_image_urls.json"
MEMES = "memes"