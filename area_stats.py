import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

dfs=pd.DataFrame()

for fname in os.listdir("."):
    if ".csv" in fname:
        print("Running script on" + (os.path.join(".", fname)))

        CSVFile=fname
        df = pd.read_csv(CSVFile)
        position=CSVFile.index('.')
        tilename=CSVFile[0:position-6]

        fig, axes = plt.subplots(2,1,sharex=True)
        axes[0].scatter(df['Bin'],df['Slp_tusc'], s=50, color="white",edgecolors="k")
        axes[0].scatter(df['Bin'],df['Slp_ntsc'], s=50, color="black")
        axes[0].set_xscale('log')
        axes[1].scatter(df['Bin'],df['Curv_tusc'], s=50, color="white",edgecolors="k")
        axes[1].scatter(df['Bin'],df['Curv_ntusc'], s=50, color="black")
        axes[1].set_xscale('log')
        axes[0].set_ylabel("Slope")
        axes[1].set_ylabel("Curvature")
        axes[1].set_xlabel("Drainage area")
        fig.suptitle(tilename)
        plt.savefig(tilename + '_plot.png')

        maxslope_a_tusc = df['Bin'][df['Slp_tusc'].idxmax()]
        maxslope_a_ntusc = df['Bin'][df['Slp_ntsc'].idxmax()]
        pos_curv_a_tusc = df['Bin'][df['Curv_tusc'] > 0.].iloc[0]
        pos_curv_a_ntusc = df['Bin'][df['Curv_ntusc'] > 0.].iloc[0]
        y_pos = df['toplefty'][0]

        data = [{'tile':tilename, 'Y Pos': y_pos, 'Area of max slope Tusc':maxslope_a_tusc, 'Area of max slope non-Tusc': maxslope_a_ntusc,
                    'Area of positive curvature, Tusc':pos_curv_a_tusc,'Area of positive curvature, non-Tusc':pos_curv_a_ntusc}]

        dfa= pd.DataFrame(data) 
        dfs =dfs.append(dfa)
        
dfs.to_csv('areastats.csv', index=False)