import matplotlib.pyplot as plt
import math
import json
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from plotmu import *
    
# make two vectors x (number of small communities) and y (NMI(mod)-NMI(map)) with data of scatter plot
def plot_scatter_data(mus, comrange,num_runs, results):
    mu = mus[-1]
    x = []
    y = []
    for com in range(len(comrange)):
        for run in range(num_runs):
            mo = results[(mu,com,'mod')][run]
            ma = results[(mu,com,'map')][run]
            diff = mo - ma
            y.append(diff)
            comsizes = results[(mu,com,str(run))]
            z = 25 #size of biggest smallest community
            
            #count number of small communities
            l = len(comsizes)
            aantal = 0
            for i in range(l):
                if 5 <= comsizes[i] <= z:
                    aantal += 1
            eig = aantal
            if eig == 0: #leave out points which have zero small communities
                y.pop()
            else:
                x.append(eig)
    return x,y

# plot number of small communities against NMI for either modularity or map equation (scatter plot)
def plot_mod_or_map(mus, comrange,num_runs, measure, results):
    mu = mus[-1]
    x = []
    y = []
    y_zero = [] # list of NMI values for graphs without small communities
    for com in range(len(comrange)):
        for run in range(num_runs):
            if measure == 'mod':
                title = 'modularity'
                mo = results[(mu,com,'mod')][run]
                y.append(mo)
            if measure == 'map':
                title = 'map equation'
                ma = results[(mu,com,'map')][run]
                y.append(ma)
            comsizes = results[(mu,com,str(run))]
            z = 25 #size of biggest smallest community
            
            #count number of small communities
            
            l = len(comsizes)
            aantal = 0
            for i in range(l):
                if 5 <= comsizes[i] <= z:
                    aantal += 1
            eig = aantal
            if eig == 0: #leave out points which have zero small communities
                y.pop()
                if measure == 'mod':
                    y_zero.append(mo)
                if measure == 'map':
                    y_zero.append(ma)
            else:
                x.append(eig)
    
    x_zero = [0]*len(y_zero)
    plt.scatter(x, y)
    plt.scatter(x_zero, y_zero, color = 'r')
    plt.title('Objective function: '+ title )
    plt.xlabel('Number of small communities')
    plt.ylabel('Normalized mutual information')
    plt.ylim(0,1)
    plt.savefig('plot'+'_scatter_'+measure+str(mu)+'.png')
    plt.show()
    return y_zero
