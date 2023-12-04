import os
import pickle
import pandas as pd

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


        