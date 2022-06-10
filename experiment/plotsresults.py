import matplotlib.pyplot as plt
import math
import json


def read_results1():
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
    

def plot_results_1(mus, comrange,num_runs, results, coms):
    if coms == 1:
        sets = [0,7,8,9]
    if coms == 2:
        sets = [0,4,5,6]
    if coms == 3:
        sets = [0,1,2,3]
    kleuren = ['k','b','r','c','m','g']
    xticks = [str(comrange[i]) for i in sets]
    x = [1, 2, 3, 4]
    kleur = 0
    for mu in mus:
        mo = []
        ma = []
        for comtype in sets:
            resultlist = results[(mu,comtype,'mod')]
            val = sum(resultlist)/num_runs
            mo.append(val)
            resultlist2 = results[(mu,comtype,'map')]
            val2 = sum(resultlist2)/num_runs
            ma.append(val2)
    plt.plot(x, mo, '-ok', label = 'modularity', color = kleuren[kleur])
    kleur += 1
    plt.plot(x, ma, '-ok', label = 'map equation', color = kleuren[kleur])
    
    plt.xticks(x, xticks)
    plt.xlabel('Community size range')
    plt.ylabel('Normalized Mutual Information')
    #plt.title('Objective function: modularity')   
    plt.legend()
    plt.ylim(0,1)
    plt.savefig('plot'+str(coms)+'.png') 
    plt.show() 
     
    

mus, comrange,num_runs, results = read_results1()
plot_results_1(mus, comrange,num_runs, results, 1)
plot_results_1(mus, comrange,num_runs, results, 2)
plot_results_1(mus, comrange,num_runs, results, 3)