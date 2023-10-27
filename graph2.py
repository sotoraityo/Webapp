from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from glob import glob
from flask import Flask, render_template,request,redirect,url_for
def csvplot(filename):
    matplotlib.use('Agg')
    plt.rcParams['figure.dpi'] = 300 

    index = 0
    #folder = r'C:\Users\sotor\OneDrive\実験用/'
    #file = glob(filename+'*csv')[index]

    #%%
    # csv読み込み
    pd_data = pd.read_csv(filename, 
                encoding = "shift-jis") # 日本語に対応


    #%%
    cols = pd_data.columns # pandasの配列の各名前を抽出

    #timestamp = pd.to_datetime(pd_data[cols[0]]) # 列の名前からデータを取得
    timestamp = pd_data[cols[0]] # 列の名前からデータを取得
    heart_rate = pd_data[cols[1]] # 心拍数

    #%%
    # プロット
    plt.figure()
    plt.plot(timestamp, heart_rate)
    plt.tight_layout()
    plt.xticks(rotation=70)

    savefolder = './static/image/'
    savefile='testgraph.png'
    plt.savefig(savefolder + savefile)

    return savefile