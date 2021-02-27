import matplotlib.pyplot as plt
import plate_loading as pl
import matplotlib.image as mpimg
from Cell import Cell
import numpy as np
import pandas as pd
from scipy.spatial import distance
from scipy.stats import pearsonr
import os
import Earth_mover_matrix as emm
from tqdm import tqdm


def save_dict_to_file(dic):
    f = open('all_wells_dict.txt', 'w')
    f.write(str(dic))
    f.close()


def load_dict_from_file():
    f = open('all_wells_dict.txt', 'r')
    data = f.read()
    f.close()
    return eval(data)


def all_dir():
    # dmso_path = "C:\\Users\\Guyza\\OneDrive\\Desktop\\Information_Systems\\Lab_Work\\" \
    #             "Cell_Communication\\Pyproject\\Wells\\DMSOs"
    #
    # dmso_plates = ["\\plate_1.1", "\\plate_1.2", "\\plate_1.3",
    #                "\\plate_2.1", "\\plate_2.2", "\\plate_2.3",
    #                "\\plate_3.1", "\\plate_3.2", "\\plate_3.3"]
    #
    # # dmso_plates = [
    # #                "\\plate_2.1", "\\plate_2.2", "\\plate_2.3",
    # #                "\\plate_3.1", "\\plate_3.2", "\\plate_3.3"]
    #
    # dmso_well_num = ["\\49", "\\50"]
    #
    # treatments_path = "C:\\Users\\Guyza\\OneDrive\\Desktop\\Information_Systems\\Lab_Work\\" \
    #                   "Cell_Communication\\Pyproject\\Wells\\treatments"
    #
    # treatments_classes = ["\\class_1\\", "\\class_2\\", "\\class_3\\"]
    # paths = [dmso_path, treatments_path]
    #
    # all_dirs = []
    # for type in paths:
    #     if "DMSO" in type:
    #         for dmso_plate in dmso_plates:
    #             for well in dmso_well_num:
    #                 all_dirs.append(type + dmso_plate + well)
    #
    #     else:
    #         for treatment_class in treatments_classes:
    #             onlydirs = [type + treatment_class + f for f in os.listdir(type + treatment_class)]
    #
    #             for dir in onlydirs:
    #                 all_dirs.append(dir)

    p = "C:\\Guy\\ordered_plates"
    plates = ["\\Plate 1.1", "\\Plate 1.2", "\\Plate 1.3",
              "\\Plate 2.1", "\\Plate 2.2", "\\Plate 2.3",
              "\\Plate 3.1", "\\Plate 3.2", "\\Plate 3.3"]

    all_dirs = []
    for plate in plates:
        all_dirs.append(p + plate)
    return all_dirs


def calculate_correlation(df):
    # calculate mean correlation as an indicator of synchronization
    corr = []
    for col in range(len(df.columns)):
        for col2 in range(col + 1, len(df.columns)):
            corr.append(df[df.columns[col]].corr(df[df.columns[col2]]))

    return corr


def compute_all_three(df):
    uniform_distribution = [1 / 50 for x in range(50)]
    names = []
    for index in range(len(df.columns)):
        names.append("cell " + str(index))
    df.columns = names

    # indicator of density of cells
    number_of_cells = len(df.columns)

    corr = calculate_correlation(df)
    mean_cor = sum(corr) / len(corr)

    # calculate earth mover's distance from the uniform distribution
    ktr_distribution = emm.correlation_per_well(df)
    dist_from_uniform = emm.earth_mover_dist(ktr_distribution, uniform_distribution)

    measurement = [number_of_cells, mean_cor, dist_from_uniform]

    return measurement


# measurements = {}
# all_dirs = all_dir()

# for path in tqdm(all_dirs):
#     try:
#         onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#         for f in onlyfiles:
#             if "ktr.xlsx" in f:
#                 io = path + "\\" + f
#                 break
#
#         ktr = pd.read_excel(io=io)
#         print(io)
#
#         measurement = compute_all_three(ktr)
#         key = path.split('\\')[-3] + "_" + path.split('\\')[-2] + "_" + path.split('\\')[-1]
#         measurements[key] = measurement
#
#
#     except:
#         print("not able to read:", path)

# for dir in tqdm(all_dirs):
#     only_ktr_files = [f for f in os.listdir(dir) if (os.path.isfile(os.path.join(dir, f)) and "ktr" in f)]
#
#     for ktr_file in only_ktr_files:
#         print(ktr_file.split('.')[0])
#         path = dir + "\\" + ktr_file
#         ktr = pd.read_excel(io=path)
#
#         measurement = compute_all_three(ktr)
#         key = ktr_file.split('.')[0]
#         measurements[key] = measurement
#
# save_dict_to_file(measurements)

read_dict = load_dict_from_file()



path = r'C:\Guy\ordered_plates\treatments_plates.csv'
t_pd = pd.read_csv(path)
t_pd = t_pd.drop(['Unnamed: 0'], axis=1)

# density = []
sync_dmso = []
sync_1 = []
sync_2 = []
sync_3 = []
dist_fron_uni_dmso = []
dist_fron_uni_1 = []
dist_fron_uni_2 = []
dist_fron_uni_3 = []
for key in read_dict:
    # x = t_pd['DMSO'].values
    if key in t_pd['DMSO'].values:
       # density.append(read_dict[key][0])
       sync_dmso.append(read_dict[key][1])
       dist_fron_uni_dmso.append(read_dict[key][2])

    elif key in t_pd['class_1'].values:
        sync_1.append(read_dict[key][1])
        dist_fron_uni_1.append(read_dict[key][2])

    elif key in t_pd['class_2'].values:
        sync_2.append(read_dict[key][1])
        dist_fron_uni_2.append(read_dict[key][2])

    elif key in t_pd['class_3'].values:
        sync_3.append(read_dict[key][1])
        dist_fron_uni_3.append(read_dict[key][2])


#
# for key in read_dict:
#     if key not in dmso_list:
#        density.append(read_dict[key][0])
#        sync.append(read_dict[key][1])
#        dist_fron_uni.append(read_dict[key][2])
#
#
# plt.scatter(sync_dmso, dist_fron_uni_dmso, c='black', label='DMSO')
plt.scatter(sync_1, dist_fron_uni_1, c='blue', label='class 1')
# plt.scatter(sync_2, dist_fron_uni_2, c='red', label='class 2')
# plt.scatter(sync_3, dist_fron_uni_3, c='green', label='class 3')
plt.legend()
plt.title("sync - dist from uniform")
plt.xlabel("mean correlation")
plt.ylabel("dist from uniform")
plt.show()

p = r'C:\Guy\ordered_plates'
wells = [r'Plate 1.3\40532', r'Plate 2.1\40520',
         r'Plate 2.2\40539', r'Plate 3.1\40506',
         r'Plate 2.1\40542']
for well in tqdm(wells):
    w = pl.load_well(os.path.join(p, well))
    w.plot_correlation_distribution(20)
