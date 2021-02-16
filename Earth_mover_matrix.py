import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.stats import wasserstein_distance


def correlation_per_well(df):
    """"outputs a list"""
    # add cell index for every column in well
    names = []
    for index in range(len(df.columns)):
        names.append("cell " + str(index))
    df.columns = names

    # calculate correlation for every pair of cells
    corr = cor(df)

    # calculate the distribution of correlations in to n bins
    ret = divide_to_n(corr, n=50)
    # ret = corr

    return ret


def divide_to_n(cor_arr, n):
    y = np.zeros(shape=(n,))
    s = len(cor_arr)

    for x in cor_arr:
        index_x = math.floor(((x + 1) / 2) * n)

        y[index_x] += 1

    res = y / s

    return res


def cor(df):
    corr = []
    length = len(df.columns)
    for first in range(length):
        for second in range(first + 1, length):
            corr.append(df[df.columns[first]].corr(df[df.columns[second]]))

    return corr


def plot(file):
    data = np.loadtxt(file)

    # names = ["dmso_1", "dmso_2", "dmso_3", "dmso_4", "dmso_5",
    #          "dmso_6", "dmso_7", "dmso_8", "dmso_9", "dmso_10",
    #          "dmso_11", "dmso_12", "dmso_13", "dmso_14", "dmso_15", "dmso_16", "dmso_17",
    #          "saracatinib", "tws119", "zm306416",
    #          "gdc0879", "sb590885",
    #          "cabozantinib", "pazopanib", "tivozanib"]
    names = ["d1", "d2", "d3", "d4", "d5",
             "d6", "d7", "d8", "d9", "d10",
             "d11", "d12", "d13", "d14", "d15", "d16", "d17",
             "class 1 sara", "class 1 tws", "class 1 zm",
             "class 2 gdc", "class 2 sb",
             "class 3 cabo", "class 3 pazo", "class 3 tivo"]

    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap='Blues')

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(names)))
    ax.set_yticks(np.arange(len(names)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(names)
    ax.set_yticklabels(names)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    # for i in range(len(names)):
    #     for j in range(len(names)):
    #         text = ax.text(j, i, data[i, j],
    #                        ha="center", va="center", color="w")

    # cax = fig.add_axes([0.27, 0.8, 0.5, 0.05])
    cax = fig.add_axes([0.8, 0.19, 0.03, 0.74])

    fig.colorbar(im, cax=cax)
    ax.set_title("wasserstein distance: " + f)

    fig.tight_layout()
    plt.show()


def earth_mover_dist(p, q):
    if len(p) != len(q):
        raise Exception("signatures not of same length!")

    emd = np.zeros(shape=(len(p) + 1,))
    for i in range(len(p)):
        emd[i + 1] = p[i] + emd[i] - q[i]

    res = sum([abs(x) for x in emd])
    return res


def make_mat():
    path = "C:\\Users\\Guyza\\OneDrive\\Desktop\\Information_Systems\\Lab_Work\\Cell_Communication\\Pyproject\\Wells\\"

    # class 1 treatments
    saracatinib_path = path + "treatments\\class_1\\saracatinib"
    tws119_path = path + "treatments\\class_1\\TWS119"
    zm306416_path = path + "treatments\\class_1\\ZM306416"

    # class 2 treatments
    gdc0879_path = path + "treatments\\class_2\\GDC0879"
    sb590885_path = path + "treatments\\class_2\\SB590885"

    # class 3 treatments
    cabozantinib_path = path + "treatments\\class_3\\cabozantinib"
    pazopanib_path = path + "treatments\\class_3\\pazopanib"
    tivozanib_path = path + "treatments\\class_3\\tivozanib"

    # DMSOs
    dmso_1_path = path + "dmsos\\plate_1.1\\49"
    dmso_2_path = path + "dmsos\\plate_1.1\\50"
    dmso_3_path = path + "dmsos\\plate_1.2\\49"
    dmso_4_path = path + "dmsos\\plate_1.2\\50"
    dmso_5_path = path + "dmsos\\plate_1.3\\49"
    dmso_6_path = path + "dmsos\\plate_1.3\\50"
    dmso_7_path = path + "dmsos\\plate_2.1\\50"
    dmso_8_path = path + "dmsos\\plate_2.2\\49"
    dmso_9_path = path + "dmsos\\plate_2.2\\50"
    dmso_10_path = path + "dmsos\\plate_2.3\\49"
    dmso_11_path = path + "dmsos\\plate_2.3\\50"
    dmso_12_path = path + "dmsos\\plate_3.1\\49"
    dmso_13_path = path + "dmsos\\plate_3.1\\50"
    dmso_14_path = path + "dmsos\\plate_3.2\\49"
    dmso_15_path = path + "dmsos\\plate_3.2\\50"
    dmso_16_path = path + "dmsos\\plate_3.3\\49"
    dmso_17_path = path + "dmsos\\plate_3.3\\50"

    w = [dmso_1_path, dmso_2_path, dmso_3_path, dmso_4_path, dmso_5_path,
         dmso_6_path, dmso_7_path, dmso_8_path, dmso_9_path, dmso_10_path,
         dmso_11_path, dmso_12_path, dmso_13_path, dmso_14_path, dmso_15_path,
         dmso_16_path, dmso_17_path,
         saracatinib_path, tws119_path, zm306416_path,
         gdc0879_path, sb590885_path,
         cabozantinib_path, pazopanib_path, tivozanib_path]

    w_mat = np.zeros(shape=(len(w), len(w)))

    for i in tqdm(range(len(w))):
        print("i: " + str(i))
        ktr_i = pd.read_excel(io=w[i] + "\\ktr.xlsx")
        ktr_i_dist = correlation_per_well(ktr_i)
        for j in range(len(w)):
            print("\tj: " + str(j))
            ktr_j = pd.read_excel(io=w[j] + "\\ktr.xlsx")
            ktr_j_dist = correlation_per_well(ktr_j)

            # w_mat[i][j] = wasserstein_distance(ktr_i_dist, ktr_j_dist)
            w_mat[i][j] = earth_mover_dist(ktr_i_dist, ktr_j_dist)

    print(w_mat)

    f = 'heatmap50bins.txt'
    np.savetxt(f, w_mat)
    print("Done!")


f = 'heatmap.txt'
# plot(f)