import matplotlib.pyplot as plt
import math
import json


def read_results2():
    f = open(r"c:\Users\veerl\OneDrive\Documenten\Mathematical Sciences\Network Science\git\NetworkScienceProject\experiment\results\mu_results.tex", 'r')
    #f = open('results\mu_results.tex', 'r')
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
    

def plot_results_2(mus, comrange,num_runs, results, eigenschap):
    # eigenschap in ['num_small', 'frac_small', 'av_size', 'range', 'num_coms', 'smallest_comsize', 'largest_comsize']
    mu = mus[-1]
    x = []
    y = []
    for com in range(len(comrange)):
    #for com in range(31, len(comrange)+31):
        for run in range(num_runs):
            mo = results[(mu,com,'mod')][run]
            ma = results[(mu,com,'map')][run]
            verschil = mo - ma
            y.append(verschil)
            comsizes = results[(mu,com,str(run))]
            
            l = len(comsizes)
            if eigenschap == 'num_small':
                aantal = 0
                for i in range(l):
                    if 5 <= comsizes[i] <= 25:
                        aantal += 1
                eig = aantal
                naam = 'Number of small communities'
            if eigenschap == 'frac_small':
                aantal = 0
                for i in range(l):
                    if 5 <= comsizes[i] <= 25:
                        aantal += 1
                eig = aantal/l
                naam = 'Fraction of small communities'
            if eigenschap == 'av_size':
                eig = sum(comsizes)/l
                naam = 'Average community size'
            if eigenschap == 'range':
                grootste = max(comsizes)
                kleinste = min(comsizes)
                eig = grootste - kleinste
                naam = 'Size of largest community - size of smallest community'
            if eigenschap == 'num_coms':
                eig = l
                naam = 'Number of communities'
            if eigenschap == 'smallest_comsize':
                eig = min(comsizes)
                naam = 'Size of smallest community'
            if eigenschap == 'largest_comsize':
                eig = max(comsizes)
                naam = 'Size of largest community'
            x.append(eig)
    plt.scatter(x, y)
    plt.xlabel(naam)
    plt.ylabel('NMI(mod)-NMI(map)')
    #plt.title('Objective function: modularity')   
    plt.ylim(-0.3,0.3)
    plt.savefig('plot'+eigenschap+'.png') 
    plt.show() 
     
    

mus, comrange,num_runs, results = read_results2()
#eigenschappen = ['num_small', 'frac_small', 'av_size', 'range', 'num_coms', 'smallest_comsize', 'largest_comsize']
eigenschappen = ['num_small', 'frac_small', 'num_coms']
for i in eigenschappen:
    plot_results_2(mus, comrange,num_runs, results, i)
