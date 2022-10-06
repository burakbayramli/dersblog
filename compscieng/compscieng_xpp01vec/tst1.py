import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

u_wind = np.load('uwind.npz')['arr_0']
v_wind = np.load('vwind.npz')['arr_0']
gi,gj = u_wind.shape
cell_count = gi*gj
area = 2000*1e9 # m2, bu alani veriyi alirken tanimlamistik
cell_area = area / cell_count

wspeedsquare = u_wind**2+v_wind**2
wspeedsquare = wspeedsquare.reshape(-1)
wspeedsquare = wspeedsquare[wspeedsquare > 30.0]
IKE = np.sum(0.5*wspeedsquare*cell_area) / 1e12
print (np.round(IKE,2), 'terrajoule')

