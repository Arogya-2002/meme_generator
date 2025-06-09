from src.exceptions import CustomException
from src.logger import logging
import sys
from src.entity.config_entity import ConfigEntity,MemeTemplatesEntity

import pandas as pd
import json
from collections import defaultdict
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class MemeTemplates:
    def __init__(self):
        try:
            self.meme_templates_config = MemeTemplatesEntity(config_entity=ConfigEntity())
            SUPABASE_URL=self.meme_templates_config.supabase_url
            SUPABASE_KEY=self.meme_templates_config.supabase_key
            self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            raise CustomException(e, sys)
        
    def fetch_table_data(self,table_name, schema="dc"):
        """Fetch all data from a Supabase table and return as DataFrame"""
        try:
            # Use the schema() method to specify the schema, then table() for the table name
            if schema != "public":
                response = self.supabase.schema(schema).table(table_name).select("*").execute()
            else:
                response = self.supabase.table(table_name).select("*").execute()
                
            if response.data:
                return pd.DataFrame(response.data)
            else:
                logging.info(f"No data found in table: {schema}.{table_name}")
                return pd.DataFrame()
        except Exception as e:
            logging.error(f"Error fetching data from {schema}.{table_name}: {e}")
            return pd.DataFrame()

    def get_emotion_images(self):
        logging.info("Fetching data from Supabase...")
        
        dialogs = self.fetch_table_data("dialogs")
        emotions = self.fetch_table_data("emotions")
        memes = self.fetch_table_data("memes_dc")
        
        if dialogs.empty or emotions.empty or memes.empty:
            logging.error("One or more tables are empty. Please check your table names and data.")
            return
        
        logging.info(f"Data fetched successfully:")
        logging.info(f"  • Dialogs: {len(dialogs)} rows")
        logging.info(f"  • Emotions: {len(emotions)} rows") 
        logging.info(f"  • Memes: {len(memes)} rows")
        
        logging.info("🔄 Merging data...")
        try:
            merged = dialogs.merge(memes, on="meme_id").merge(emotions, on="emotion_id")
            emotion_images = merged[["emotion_label", "image_path"]].dropna().drop_duplicates()

            if emotion_images.empty:
                logging.error("No valid emotion-image pairs found after merging.")
                return

            logging.info(f"Found {len(emotion_images)} unique emotion-image pairs")

        except KeyError as e:
            logging.error(f" Column not found during merge: {e}")
            logging.debug(f"  • Dialogs columns: {list(dialogs.columns)}")
            logging.debug(f"  • Emotions columns: {list(emotions.columns)}")
            logging.debug(f"  • Memes columns: {list(memes.columns)}")
            return

        emotion_to_urls = defaultdict(list)
        for _, row in emotion_images.iterrows():
            emotion = row["emotion_label"]
            filename = os.path.basename(row["image_path"])
            full_url = f"{self.meme_templates_config.supabase_url}/storage/v1/object/public/{self.meme_templates_config.bucket_path}/{filename}"
            emotion_to_urls[emotion].append(full_url)

        emotion_to_urls = dict(emotion_to_urls)

        # Ensure 'artifacts' directory exists
    
        os.makedirs(self.meme_templates_config.output_dir, exist_ok=True)
        output_file = os.path.join(self.meme_templates_config.output_dir, self.meme_templates_config.json_file)

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(emotion_to_urls, f, indent=2, ensure_ascii=False)
            logging.info(f"Image URLs successfully saved to: {output_file}")
        except Exception as e:
            logging.error(f"Failed to write JSON to {output_file}: {e}")
            return

        total_urls = sum(len(urls) for urls in emotion_to_urls.values())
        logging.info(f"Summary: {len(emotion_to_urls)} emotions with {total_urls} total image URLs")
        logging.info("Sample emotions and URL counts:")
        for emotion, urls in list(emotion_to_urls.items())[:5]:
            logging.info(f"  • {emotion}: {len(urls)} images")

if __name__ == "__main__":
    meme_temp = MemeTemplates()
    meme_temp.get_emotion_images()
