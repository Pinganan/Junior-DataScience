
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

def create_data():
    df = pd.read_excel("../dataset/GDP_original.xlsx")
    df = df.fillna(value=0)
    year_GDP = {"Year" : "million_dollars"}
    for row in range(2, 2+9):
        year_GDP[int(df.iloc[row][0])-1911] = df.iloc[row][1]
    # 指定orient='index'使用字典鍵作為行來創建DataFrame
    pd.DataFrame.from_dict(data=year_GDP, orient='index').to_excel('../dataset/GDP.xlsx', header=False)

def draw_2D_graph():
    plt.style.use('classic')
    gdp_data = pd.read_excel("../dataset/GDP.xlsx")
    crime_data = pd.read_excel("../dataset/犯罪事件.xlsx")
    ##GDP & crime
    plt.figure()
    fig, ax1 = plt.subplots()
    
    #標題
    plt.suptitle('GDP vs crime')
    #X軸名稱
    ax1.set_xlabel('Year')
    #直方圖及左側Y軸名稱
    ax1.bar(crime_data.iloc[:,0], crime_data.iloc[:,1], color='steelblue', label='crime(left)')
    ax1.tick_params('y', colors='darkslategray')
    #相同x軸
    ax2 = ax1.twinx()
    #折線圖及右側Y軸名稱
    ax2.plot(gdp_data.iloc[:,0], gdp_data.iloc[:,1], color='maroon', label='GDP(right)')
    ax2.tick_params('y', colors='maroon')
    #圖例
    ax1.legend(loc='upper left', shadow=True)
    ax2.legend(loc='upper center', shadow=True)
    plt.show()

def draw_3D_graph():
    df_GDP = pd.read_excel('../dataset/GDP.xlsx')
    df_Crime = pd.read_excel('../dataset/犯罪事件.xlsx')
    #設定key
    key_GDP = df_GDP.keys()[1]
    key_Crime = df_Crime.keys()[1]
    #資料集裡的最小值
    min_GDP = min(df_GDP[key_GDP])
    min_Crime = min(df_Crime[key_Crime])
    #將資料以百分比的方式呈現
    av_GDP = (max(df_GDP[key_GDP]) - min_GDP) / 100
    av_Crime = (max(df_Crime[key_Crime]) - min_Crime) / 100
    for i in range(9):
        df_GDP[key_GDP][i] = (df_GDP[key_GDP][i]-min_GDP)/av_GDP
        df_Crime[key_Crime][i] = (df_Crime[key_Crime][i]-min_Crime)/av_Crime
    #轉換成 ndarray
    df_GDP_np = df_GDP[key_GDP].to_numpy()
    df_Crime_np = df_Crime[key_Crime].to_numpy()
    data = np.array([df_GDP_np, df_Crime_np],dtype=int)
    # 保持間隔的命名
    column_names = range(99,110,2)
    row_names = ['','','GDP','','','','Crime','','']

    fig = plt.figure()
    # 三維的軸
    ax = Axes3D(fig)
    # x, y軸的資料量
    len_x, len_y = 9, 2
    # 用描述資料大小
    xpos = np.arange(0,len_x,1)
    ypos = np.arange(0,len_y,1)
    xpos, ypos = np.meshgrid(xpos, ypos)
    # 攤平資料，變成一維
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(len_x * len_y)
    # 資料間隔
    dx = 0.75 * np.ones_like(zpos)
    dy = dx.copy()
    dz = data.flatten()
    # 用顏色標示資料間的差異
    colors = plt.cm.jet(data.flatten()/float(data.max()))
    ax.bar3d(xpos,ypos,zpos, dx, dy, dz, color = colors, alpha = 0.4)   # alpha為透明度
    # x, y軸的標示
    ax.w_xaxis.set_ticklabels(column_names)
    ax.w_yaxis.set_ticklabels(row_names)
    ax.set_xlabel('Year')
    ax.set_ylabel('Data')
    ax.set_zlabel('%')
    plt.show()

#create_data()
#draw_2D_graph()
draw_3D_graph()