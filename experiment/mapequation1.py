import networkx as nx
import math
import numpy as np
import sklearn
from sklearn.preprocessing import normalize


'Compute probability of being in community i'
'From paper, this is p^i_arrow, without the q term'
def p_arrow(communities, p, i): 
    result = 0
    if len(list(communities)[i])==0:
            return 0
    for node in list(communities)[i]:
        result += p[node]
    return result

'Calculates the vector q, where q_i is the probability to leave community i'
def calculate_q(graph, communities, p):
    q = []
    
    def calculate_qi(alpha):
        if len(list(communities)[alpha])==0:
            return 0
        result = 0
        edges_uit=0
        degrees = 0
        for node in list(communities)[alpha]:
            degrees += graph.degree[node]
            for neighbour in list(graph.neighbors(node)):
                if neighbour not in list(communities)[alpha]:
                    edges_uit += 1
        result = edges_uit / degrees
        
        return p_arrow(communities, p, alpha) * result
    
    for i in range(len(communities)):
        qi = calculate_qi(i)
        q.append(qi) 
        
    # print('Dit is q:', q)   
    # print('som q:',sum(q))
    return q   

'Calculate the vector p, where p_i is the probability to be in node i'
def calculate_p(graph): 

    'Get adjacency matrix and normalize, such that columns sum to 1'
    A = nx.to_numpy_matrix(graph)
    A = normalize(A, axis=0, norm='l1') 
    
    'Initialize p, equal probability to start in every node'
    n = graph.number_of_nodes()
    p = np.empty
    p = np.full((n,1), 1/n)
    
    'Performs a max of 100 iterations, unless convergence is met earlier (within a given error tolerance)'
    for i in range(100): 
        previous = p
        p = np.matmul(A,p)        
        if np.allclose(previous,p, rtol = (1.e-5)/n): 
            return p.flatten().tolist()
    
    return p.flatten().tolist()

'Help function'
def a_log_a(a):
    if a == 0:
        return 0
    else:
        return a*math.log(a,2)
    
'The final map equation, as equation (4) from paper'
def map_equation2(graph, communities, p):
    q = calculate_q(graph, communities, p)
    result = a_log_a(sum(q))
    
    term = 0
    for i in range(len(communities)):
        term += a_log_a(q[i])
    
    term2 = 0
    for alpha in list(graph.nodes()):
        term2 += a_log_a(p[alpha])
    
    term3 = 0
    for i in range(len(communities)):
        a = q[i]+ p_arrow(communities, p, i)
        term3 += a_log_a(a)

    result += -2*term -term2 + term3
    
    return result

'Generate graph, list of ground-truth communities and vector p'
#graph = LFR(100, 2.5, 2.5, 0.2,10, 40)
#communities = list({frozenset(graph.nodes[v]["community"]) for v in graph})
#p = calculate_p(graph)

#q = calculate_q(graph,communities,p)

'Calculate value of map equation of ground-truth communities'
#print('mapeq2:', map_equation2(graph, communities, p))
