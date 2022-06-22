import matplotlib.pyplot as plt
import math
import json
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm


def read_results2():
    "Write your own path here to read results"
    # f = open(r"c:\Users\veerl\OneDrive\Documenten\Mathematical Sciences\Network Science\git\NetworkScienceProject\experiment\results\mu_results.tex", 'r')
    f = open('results\mu_results.tex', 'r')
    lines = f.readlines()

    #find mus
    mus1 = list(lines[0].split(','))
    mus1.pop()
    print(mus1)
    mus= [float(mu) for mu in mus1]
    
    #find com sizes
    comrangelist = lines[1].split(',')
    comrangelist.pop()
    comrange = [[int(comrangelist[i]), int(comrangelist[i+1])] for i in range(0,len(comrangelist), 2)]
    
    #find num_runs
    num_runs = int(lines[2])

    #find results
    results ={}
    for line in lines[3:]:
        linessplit = line.split(":")
        input_string = linessplit[0].split(",")

        output_string = linessplit[1].split(",")
        output_string.pop()
        
        input = (float(input_string[0]), float(input_string[1]), input_string[2])
        output = [float(x) for x in output_string]
        
        results[input] = output
    
    f.close()
        
    return mus, comrange,num_runs, results
    
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
def plot_mod_or_map(mus, comrange,num_runs, measure):
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
              
    plt.scatter(x, y)
    plt.title('Objective function: '+ title )
    plt.xlabel('Number of small communities')
    plt.ylabel('Normalized mutual information')
    plt.ylim(0,1)
    plt.savefig('plot'+'_scatter_'+measure+str(mu)+'.png')
    plt.show()
    return y_zero
     
    

# from here, the scatter plot of NMI(mod)-NMI(map) against the number of small communities is made, including regression
# read results
mus, comrange,num_runs, results = read_results2()

# get data for scatter plot
x,y = plot_scatter_data(mus, comrange,num_runs, results)
x = np.array(x).reshape((-1,1))
y = np.array(y)

# start regression
model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
print(f"coefficient of determination: {r_sq}")
print(f"intercept: {model.intercept_}")
print(f"slope: {model.coef_}")

def regressie(x, intercept, coef):
    return x*coef+intercept

# make scatter plot, including regression
plt.scatter(x, y)
plt.plot(x, regressie(x,model.intercept_, model.coef_[0]), color = 'r', label='y='+str(round(model.coef_[0],5))+'x+'+str(round(model.intercept_,5)))
plt.xlabel('Number of small communities')
plt.ylabel('NMI(mod)-NMI(map)')  
plt.ylim(-0.3,0.3)
plt.legend()
plt.title('R-squared value: '+str(round(r_sq,5)))
plt.savefig('plot'+'_num_small_'+'regressie'+str(mus[-1])+'.png') 
plt.show() 

# make plots for modularity and map equation seperately
plot_mod_or_map(mus, comrange,num_runs, 'map')
plot_mod_or_map(mus, comrange,num_runs, 'mod')
