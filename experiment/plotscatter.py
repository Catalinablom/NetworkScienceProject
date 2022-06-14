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
    # eigenschap in ['num_small', 'frac_small', 'av_size', 'range', 'num_coms']
    x = []
    y = []
    for com in comrange:
        verschil = results[(mu,com,'mod')]-results[(mu,com,'map')] #doet hij nu getallen van elkaar afhalen of lijsten?
        y.append(verschil)
        x.append(results[(mu, com, eigenschap)])
    plt.scatter(x, y)
    plt.xlabel(eigenschap) #verander dit naar een heel woord
    plt.ylabel('NMI(mod)-NMI(map)')
    #plt.title('Objective function: modularity')   
    plt.ylim(-1,1)
    plt.savefig('plot'+eigenschap+'.png') 
    plt.show() 
     
    

mus, comrange,num_runs, results = read_results2()
eigenschappen = ['num_small', 'frac_small', 'av_size', 'range', 'num_coms']
for i in eigenschappen:
    plot_results_2(mus, comrange,num_runs, results, i)
