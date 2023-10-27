from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

def double(n):
     return n*0.002

def csvplot(filename):
    matplotlib.use('Agg')
    plt.rcParams['figure.dpi'] = 300 

    #index = 0
    #folder = r'C:\Users\sotor\OneDrive\実験用/'
    #file = glob(filename+'*csv')[index]

    #%%
    # csv読み込み
    pd_data = pd.read_csv(filename, 
                encoding = "shift-jis") # 日本語に対応


    #%%
    cols = pd_data.columns # pandasの配列の各名前を抽出
    pd_data[cols[0]]=pd_data[cols[0]]*0.002
    #timestamp = pd.to_datetime(pd_data[cols[0]]) # 列の名前からデータを取得
    #id = pd_data[cols[0]] # 列の名前からデータを取得
    timestamp=pd_data[cols[0]]
    heart_rate = pd_data[cols[2]] # 心拍数
    bpm = pd_data[cols[3]] # bpm

    
    plt.rcParams['font.family'] = "MS Gothic"
 
    #%%
    # プロット
    Figure, ax1=plt.subplots()
    ax2=ax1.twinx()

    ax1.plot(timestamp, heart_rate,color='red',label="心拍数")
    #ax1.set_xlim([0,100])
    ax1.set_ylim([0,1300])

    ax2.plot(timestamp,bpm,color='blue',label="bpm")
    #ax2.set_xlim([0,100])
    #ax2.set_ylim([40,100])

    #plt.title('心拍数とbpm')
    ax2.spines['left'].set_color('red')
    ax2.spines['right'].set_color('blue')

    ax1.tick_params(axis='y', colors='red')
    ax2.tick_params(axis='y', colors='blue')

    handler1, label1 = ax1.get_legend_handles_labels()
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler1 + handler2, label1 + label2,
                loc=2, borderaxespad=0.)
    """
    plt.figure()
    plt.plot(timestamp, bpm)
    plt.tight_layout()
    plt.title('bpm')
    plt.xticks(rotation=70)
    """

    savefolder = './static/image/graph/'
    savefile='testgraph.png'
    plt.savefig(savefolder + savefile)

    return savefile