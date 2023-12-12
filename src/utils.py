import os
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_samples,silhouette_score


def load_object(file_path):
    try:

        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                # while True:
                #     try:
                        # yield pickle.load(file)
                    # except EOFError:
                    #     break
            # return {}
                return pickle.load(file)
        else:
            return {},{},{},{}

    except Exception as e:
        pass

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok= True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        pass


def save_data(file_path, data):
    # try:
    pass

def convert_time_to_min(time_list):
    total_time = 0
    for time in time_list:
        total_time += time.total_seconds() // 60
    return total_time

def get_freq(time_list):
    return len(time_list)

def scale(click,del_t,Type):
#     match Type:
    if Type == 'polynomial':
        return click + del_t/10
    elif Type == 'log':
        return click + np.log(del_t)
    elif Type == 'exp1':
        return click * (1 - np.exp(-del_t))
    else:
        return click + del_t
    

        