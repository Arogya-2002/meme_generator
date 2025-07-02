from dataclasses import dataclass

@dataclass
class TopicIngestionArtifact:
    """
    Represents the artifact for topic ingestion.
    """
    topic_name: str



@dataclass
class EmotionAnalyzerArtifact:
    """
    Represents the artifact for emotion analysis.
    """
    emotion_name:str

@dataclass
class MemesDialogsGeneratorArtifact:
    """
    Represents the artifact for memes dialogs generation.
    """
    generated_dialogs: str