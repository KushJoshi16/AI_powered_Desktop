import os
from dataclasses import dataclass



@dataclass
class DataIngestionConfig:
    data_path: str=os.path.join('metadata','metadata.pkl')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        pass
            
 