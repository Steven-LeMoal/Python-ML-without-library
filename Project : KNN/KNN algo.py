#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mai 2 13:15:17 2022

@author: steven
"""

import panda as pd

class Objet():
    def __init__(self,val,classe = ''):
        self.coordonnées = val
        self.classe = classe
    def __str__(self):
        return f"x : {self.x}; y : {self.y} ; z : {self.z} ; t : {self.t} ; classe : {self.classe}"
    def distance(self,autre):
        return ((self.coordonnées - autre.coordonnées)**2)**(1/2)
    def set_classe(self, a):						 		 	 	 		 	 
        self._classe = a				 		 	 	 		 	 

def Exo1():
    
    """
    Question 1:
        le calcul de la distance
        
    Question 2:
        Imaginons que l'on met en entré pour chaque individu on metant sa classe et 3 sur 4 de ses attributs (valeurs)
        On va essayer de déduire le 4eme attribut (valeur)
        Plein d'autre chose ex : attribuer une valeur a chaque classe et déduire la valeur de la classe d'un individu a partir des données
        
    Question 3:
    """
    
    f = pd.read_csv('data.txt',sep=';',header= None)
    k = int(input("Veuillez saisir la valeur de k : "))
    test_tab = [input(f"Veuillez sasir la valeur {i} : ") for i in range(4)]
    test = Objet(test_tab)
    distance = dict()
    for line in f:
        ele = line.replace('\n','').split(',')
        distance[str(test.distance(Objet(ele,ele[4])))] = ele[4]
    select = list(dict(sorted(distance.items(), key=lambda kv: kv[1])).values())[:k]
    test.classe = (max(select, key=select.count))
    print("\n",test)
        
              



# %% zone du main
if __name__ == '__main__' :
    Exo1()