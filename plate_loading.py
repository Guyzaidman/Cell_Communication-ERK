import os
import pandas as pd
from tqdm import tqdm
from Well import Well
import pickle


def load_well(path):
    """
    returns a Well object constructed from the given path
    :param path: a path to the directory where there are ktr.xlsx, x.xlsx and y.xlsx files
    :return: Plate object
    """
    try:
        ktr_df = pd.read_excel(os.path.join(path, "ktr.xlsx"), header=None)
        x_df = pd.read_excel(os.path.join(path, "x.xlsx"), header=None)
        y_df = pd.read_excel(os.path.join(path, "y.xlsx"), header=None)

        name = path.split('\\')[-2:]
        name = name[0] + "_" + name[1]

        return Well(ktr_df, x_df, y_df, name)

    except:
        print("not found")
        pass


def load_plate(path):
    wells = []
    for root, directories, filenames in os.walk(path):
        for d in tqdm(directories):
            w = load_well(os.path.join(root, d))
            if w is not None:
                wells.append(w)
        break
    return wells


def saving_pickle_obj(path, name, obj):
    """
    save object using pickle protocol
    :param path: String, path to desired directory
    :param name: String, object name
    :param obj: Object, object to save
    :return: -
    """
    s = os.path.join(path, name + '.obj')
    with open(s, 'wb') as f:
        pickle.dump(obj, f)


def load_pickle_obj(path, name):
    """
    load object using pickle protocol
    :param path: String, path to desired directory
    :param name: String, object name
    :return: desired object
    """
    s = os.path.join(path, name + '.obj')
    with open(s, 'rb') as f:
        o = pickle.load(f)
        return o
