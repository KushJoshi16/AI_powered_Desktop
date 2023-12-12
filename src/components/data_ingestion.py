import os
from dataclasses import dataclass
from src.utils import load_object, convert_time_to_min, get_freq, scale
import pandas as pd



@dataclass
class DataIngestionConfig:
    data_path: str=os.path.join('metadata','metadata.pkl')


class DataIngestion:
    """
        DataIngestion class is contains member function to get data and process it into a pandas dataframe.
        The dataframe consist of columns having folder id, folder coordinates.

    """
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """
        Data ingestion is a class 
        """
        obj = load_object(self.ingestion_config.data_path)
        df = pd.DataFrame.from_dict(obj[1])
        # df.T.reset_index().columns.values
        df = df.transpose().reset_index().rename(columns = {'index':'folder_id',0: 'time',1: 'status',2: 'coordinates' })
        df[['x', 'y']] = pd.DataFrame(df['coordinates'].tolist(), index=df.index)
        # df.time.explode()
        df['del_T'] = df.time.apply(convert_time_to_min)
        df['click'] = df.time.apply(get_freq)
        X = df.iloc[:,[0,-2,-1]]
        # X['utility'] = X.apply(lambda x: scale(x.click, x.del_T,'exp1'), axis=1)
        return X
    
            
 
if __name__ == "__main__":
    # config = DataIngestionConfig()
    ingestion = DataIngestion()
    X = ingestion.initiate_data_ingestion()
    print(X)




    