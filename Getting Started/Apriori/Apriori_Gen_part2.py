#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 10:58:20 2022

@author: steven
"""

def Apriori(T,eps):
    L=[]
    singleton = set(sum(T,[]))
    L.append([ [x] for x in singleton])
    #print(L)
    i=1
    k=1
    while len(L[k-1])>0:
        Ck =[]
        for a in L[k-1]:
            for b in singleton:
                if b not in a and len(a)+1==k+1 and all(not all(d in c for d in a+[b]) for c in Ck) :
                    Ck.append((a+[b]))
                    
        d={}
        for t in T:
            Dt = [c for c in Ck if all(a in t for a in c)]            
            for c in Dt:
                clef = "-".join([str(i) for i in c])
                if clef in d.keys():
                    d[clef]+=1
                else:
                    d[clef]=1        
        print(d)
        print("Level",i,":",*L[k-1])        
        i+=1
        L.append([[int(a) for a in c.split('-')] for c in d.keys() if d[c]>=eps])
        k+=1
    return L

t1 = [1, 2, 5]
t2 = [1, 3 ,5]
t3 = [1, 2]
t4 = [1, 2, 3, 4, 5]
t5 = [1, 2, 4, 5]
t6 = [2, 3, 5]
t7 = [1, 5]

T=[t1,t2,t3,t4,t5,t6,t7]
i=1
Apriori(T,3)
