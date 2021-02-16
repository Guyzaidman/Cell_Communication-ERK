import os
import pandas as pd
import matplotlib.pyplot as plt

path = "C:\\Users\\Guyza\\OneDrive\\Desktop\\Information_Systems\\Lab_Work\\Cell_Communication\\Pyproject\\Wells" \
       "\\DMSOs\\"

plates = ["plate_1.1", "plate_1.2", "plate_1.3",
          "plate_2.1", "plate_2.2", "plate_2.3",
          "plate_3.1", "plate_3.2", "plate_3.3"]

well_num = ["\\49", "\\50"]

for plate in plates:
    print(plate)
    for well in well_num:

        io = path + plate + well
        # io = path + "plate_1.2" + "\\49"
        if not os.path.isdir(io):
            continue

        print("\t" + well)

        ktr = pd.read_excel(io=io + "\\ktr.xlsx")

        names = []
        for index in range(len(ktr.columns)):
            names.append("cell " + str(index))
        ktr.columns = names

        # for c in ktr.columns:
        #     ktr[c] = ktr[c].pct_change()

        corr = []
        for col in range(len(ktr.columns)):
            for col2 in range(col + 1, len(ktr.columns)):
                corr.append(ktr[ktr.columns[col]].corr(ktr[ktr.columns[col2]]))

        # print(corr)
        well_name = plate + well
        plt.title(well_name)
        plt.hist(corr, bins=50)
        plt.show()
        # plt.savefig(well_name.replace("\\", "_") + "_percentage.png")
        # plt.clf()
