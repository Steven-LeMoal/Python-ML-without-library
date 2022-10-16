#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 09:17:12 2022

@author: steven
"""

def Apriori(T,e):
    L = []
    L.append({s for t in T for s in t})
    #print(L)
    k = 1
    while k <= len(L[0]):
        C = Apriori_Gen(L,T,k)
        D = {}
        for x in C:
            D[x] = sum(set(list(x)).issubset(set(t)) for t in T) 
        print("\nLevel",k-1,":",*sorted(L[k-1]))
        print(dict(sorted(D.items())))
        k += 1
        L.append({x for x in C if D[x] >= e})
    return L
        
def Apriori_Gen(L,T,k):
    if k == 1:
        return L[0]
    else:
        C = set()
        for l in L[k-1]:
            for s in L[0]:
                if s not in l and s is not l:
                    C.add("".join(sorted(str(l)+s)))
                    #trier le string permet au set de ne pas mettre nativement les combinaison similaire mais d'ordre différent
        return set(sorted(C))
        

if __name__=='__main__':
    
    with open(r'/Users/steven/Documents/ESILV/IA & Data/dataset.txt','r') as f:
        T = [line.replace('\n','').split(', ') for line in f]
        #print(T)
        L = Apriori(T, 3)