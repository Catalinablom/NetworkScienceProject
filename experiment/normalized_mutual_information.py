# -*- coding: utf-8 -*-

import math

def delta(a, b):
    if a == b:
        return 1
    else:
        return 0
    
def P(t, g, T, G): #P(T|G)

    sum_teller = 0
    sum_noemer = 0
    
    for i in range(len(t)):
        sum_teller += (delta(t[i], T) * delta(g[i], G))
        sum_noemer += delta(g[i], G)
    
    if sum_noemer == 0:
        return 0
    
    return sum_teller / sum_noemer

def Pe(g, G): #P(G)
    n = len(g)
    som = 0
    for i in range(len(g)):
        som += (delta(g[i], G) / n)
    return som

def H(t, g): #H(t|g)
    som = 0
    for ge in range(max(g)+1): # over all communities of g, ervanuitgaande dat de communities van 0, c (max(g)) genummerd zijn
        som2 = 0
        for te in range(max(t)+1): # over all communities of t, ervanuitgaande dat de communities van 0, c (max(t)) genummerd zijn
            if P(t, g, te, ge) == 0:
                som2 += 0
            else:
                som2 += (P(t, g, te, ge) * math.log(P(t, g, te, ge),2))
        som += (Pe(g, ge) * som2)
    return -1*som

def Ha(t): #H(t)
    som = 0
    for i in range(max(t)+1): # over alle communities van t, ervanuitgaande dat de communities van 0, c genummerd zijn
        if Pe(t,i) == 0:
            som += 0
        else:
            som += (Pe(t,i) * math.log(Pe(t,i),2)) 
    return -1*som


#Compares found solution to ground truth (between -0.5 and 1, where higher is better)
def norm_mutual_inf(t, g): 
    # t is vector with t_i community of node i in ground truth
    # g is vector with g_i community of node i by algorithm
    teller = 2*(Ha(t) - H(t,g))
    noemer = Ha(t) + Ha(g)
    if noemer == 0:
        return 0
    
    return teller / noemer

