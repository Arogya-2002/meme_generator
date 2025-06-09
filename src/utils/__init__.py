import uuid
from datetime import datetime
import re

def generate_unique_filename(topic_name: str, extension="png") -> str:
    # Slugify the topic (remove special characters and spaces)
    topic_slug = re.sub(r'[^a-zA-Z0-9]+', '_', topic_name.strip().lower())
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_id = uuid.uuid4().hex[:6]  # 6-char unique suffix

    filename = f"{topic_slug}_{timestamp}_{random_id}.{extension}"
    return filename