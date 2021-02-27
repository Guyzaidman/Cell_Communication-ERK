import os
from math import sqrt
import pandas as pd
from tqdm import tqdm
from Well import Well
import pickle


# def DTWDistance(s1, s2):
#     DTW = {}
#
#     for i in range(len(s1)):
#         DTW[(i, -1)] = float('inf')
#     for i in range(len(s2)):
#         DTW[(-1, i)] = float('inf')
#     DTW[(-1, -1)] = 0
#
#     for i in range(len(s1)):
#         for j in range(len(s2)):
#             dist = (s1[i] - s2[j]) ** 2
#             DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])
#
#     return sqrt(DTW[len(s1) - 1, len(s2) - 1])


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
        for dir in tqdm(directories):
            w = load_well(os.path.join(root, dir))
            if w is not None:
                wells.append(w)
        break
    return wells


# p = r'C:\Users\Guyza\OneDrive\Desktop\Information_Systems\Lab_Work\Cell_Communication\Pyproject\Wells\DMSOs\plate_1.1\49'
p = "C:\\Guy\\ordered_plates\\Plate 1.1\\40506"
# p = "C:\\Guy\\ordered_plates"
directories = ['Plate 1.1', 'Plate 1.2', 'Plate 1.3',
               'Plate 2.1', 'Plate 2.2', 'Plate 2.3',
               'Plate 3.1', 'Plate 3.2', 'Plate 3.3',]

# directories = ['Plate 2.1']
# plates = {}
# for dir in directories:
#     print("loading " + dir)
#     plates[dir] = load_plate(os.path.join(p, dir))
#
# print('done loading')

# Step 2
# for k in plates:
#     n = os.path.join(p, k + '.obj')
#     with open(n, 'wb') as config_dictionary_file:
#         # Step 3
#         pickle.dump(plates[k], config_dictionary_file)

print('Done!!!')

# for k in plates:
#     for w in plates[k]:
#         for c in w.cells:
#             print(c.id)
#             c.plot_ktr()
#             print(c.get_cell_position(100))
#             print(c.number_of_frames)
#             print("\n------------\n")


x = load_well(p)
x.plot_correlation_distribution(n=33)
print()

# ---------------------------------------------------

# names = ['405_0' + str(i) for i in range(1, 10)]
# names.extend(['405_' + str(i) for i in range(10, 51)])
#
#
# for name in names:
#     for root, directories, filenames in os.walk(p):
#         for dir in directories:
#             src = os.path.join(p, dir)
#             dest = os.path.join(p, dir.replace('_', ''))
#             os.rename(src, dest)
#         print('done')
#
# print()
