from src.exceptions import CustomException
from src.logger import logging
from src.entity.config_entity import ConfigEntity, TopicIngestionConfigEntity
from src.entity.artifact_entity import TopicIngestionArtifact

import os
import sys

class TopicIngestion:
    def __init__(self):
        try:
            self.topic_ingestion_config = TopicIngestionConfigEntity(config_entity=ConfigEntity())
        except Exception as e:
            raise CustomException(e, sys)
    def initiate_topic_ingestion(self, topic: str) -> TopicIngestionArtifact:
        try:
            logging.info("Topic ingestion started")

            if not topic or topic.strip() == "":
                raise ValueError("Provided topic is empty.")

            if topic == self.topic_ingestion_config.topic_name:
                raise ValueError("Provided topic matches the existing configured topic.")

            logging.info(f"Ingesting topic: {topic}")


            return TopicIngestionArtifact(topic_name=topic)

        except Exception as e:
            raise CustomException(e, sys)

# if __name__ == "__main__":
#     try:
#         topic_ingestion = TopicIngestion()
#         topic_name = "exam failed"  # Replace with actual topic input
#         artifact = topic_ingestion.initiate_topic_ingestion(topic_name)
#         print(f"Topic ingestion completed successfully: {artifact}")
#     except Exception as e:
#         raise CustomException(e, sys)