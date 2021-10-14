import os
import pandas as pd
from tqdm import tqdm
from Well import Well
import pickle
from scipy.spatial import distance
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from statistics import mean


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
        name[0] = name[0].replace(' ', '_').replace('.', '-').lower()
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


def load_all_plates(path):
    plates = {}
    for root, directories, filenames in os.walk(path):
        for d in directories:
            try:
                plates[d] = load_plate(os.path.join(path, d))
            except:
                pass
        break

    return plates


def save_pickle_obj(path, name, obj):
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


# p = r'C:\Guy\ordered_plates'
# plate = load_pickle_obj(p, 'Plate 1.1')
#
# for well in range(50):
#     w = plate[well]
#     s = pd.Series()
#     for i in range(121):
#         summ = 0
#         for c in w.cells:
#             summ += c.ktr[i]
#
#         s._set_value(i,summ/len(w.cells))
#
#     s.plot()
#     plt.title(w.well_name)
#     plt.show()




