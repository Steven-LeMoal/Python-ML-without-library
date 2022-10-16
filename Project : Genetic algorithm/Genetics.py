# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 19:25:06 2022

@author: steven
"""
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import time


number_opti = 3
#nombre de parent par population sélectionné est mise à jour dans le main
nombre_parent_pop = 0
#nombre de nouvelle population généré chaque génération est mise à jour dans le main
new_pop_generation = 2
#last (mauvaise population selectionnée pour les mutations) est mise à jour dans le main
last = 0
#precision en valeur significative (faire attention en dépassement du à l'écriture scientifique puissance e : peut être résolue)
precision = 4
#pourcentage qu'un gène soit selctionné pour une mutation (*il y a un cas particulier)
pourcentage_mutation = 0.1
#pourcentage qu'un individu soit selectionné pour participer au mutation
pourcentage_select_mutation = 0.1
#pourcentage qu'un individu soit selectionné pour participer au croissemnt
pourcentage_select_croissement = 0.6
#pourcentage qu'un gène soit selctionné pour un croissement (*il y a un cas particulier)
pourcentage_croissement = 0.7
#erreur à partir de laquelle on arrète l'algorithme (condition enlever du while de Solutions possibles pour test particulier)
erreur = 0.1


dataset = []

# %% zone de la classe
#faire deux truc séparement une ia pour x et l'autre pour y
class Individu:
    def __init__(self, index,vals = None):
        if vals == None:
            self.val = [round(random.uniform(-100, 100),precision) for i in range(number_opti)]
        else:
            self.val = vals
        self.index = index
        self.distance = self.fitness(index)
        
    def __str__(self):
        repre = "x" if self.index == 1 else "y"
        return ",".join([f"({repre}{i} : {j})" for i,j in zip(range(number_opti),self.val)])
    
    def get_erreur(self):
        return self.distance
    
    def get_val(self):
        return self.val
    
    def fitness(self,index):
        dif = []
        for i in range(len(dataset)):
          t = tab[i][0]
          value = fct(self.val,t)
          dif.append(pow((value - dataset[i][index]),2))
        return moyenne(dif)
    
    def create_rand_pop(count,index):
        return [Individu(index) for i in range(count)]
    
    def evaluate(pop):
        return list(sorted(pop, key = lambda ele: ele.distance))
    
    def selection(pop, nb_parent,last):
        return pop[:nb_parent], pop[-last:]
    
    def croisement(ind1,ind2,index):
        enfant1 = []
        enfant2 = []
        #on fait un petit aléatoire pour savoir quelle gène on croisse
        for a,b in zip(ind1.val,ind2.val):
       
            if random_number(0,1,True) < pourcentage_croissement:
                a_i , b_i = generatione_select(a, b)
                enfant1.append(a_i)
                enfant2.append(b_i)
            else:
                enfant1.append(a)
                enfant2.append(b)

        return [Individu(index,enfant1),Individu(index,enfant2)]
    
    def mutation(ind):
        #on rajoute des test aléatoires pour faire varier au maximum lesindividus et génes touchés ainsi que 'la puissance' de la mutation
        i = 0
        for ele in ind.val:
            if random.uniform(0, 1) < pourcentage_mutation:
                #on peut facilement déduire que la valeur qui sera la plus chaotic sera p3 ou p6 dans le sinus donc on fait un cas particulier pour les 2
                if random.uniform(0, 1) < pourcentage_mutation*4:
                    
                    if random_number(0,1) < 0.5:
                        ele *= random_number(0,1.5)
                        
                        if i == 2:
                            ele = random.uniform(-100,100)
                    else:
                        ele += random_number(0,1.5)
                i = i + 1
                
                if(abs(ele) > 100):
                    ele = random.uniform(-100,100) if ele > 100 or ele < -100 else ele
        return ind

#pas vraiment la moyenne plutot, elle ressemble à laa racine carré de le variance S* = racine_carré de la somme (N) des différences au carré sur N
def moyenne(dif):
    somme = sum(dif)
    return pow((somme/(len(dif)-1)),1/2)


def fct(value,t):
    return value[0] * math.sin(value[1] * t + value[2])

#one-point crossover selection est le mieux pour la convergenerationce vers une solution dans notre problème
def generatione_select(a,b):
    #on prend quelques précotion en fonction de la precision qu'on veut (attention à l'écriture scientifique ex : 10e-15)
    a_entiere, a_deci = '{0:.{prec}f}'.format(a, prec = precision).replace('-','').split('.')
    b_entiere, b_deci = '{0:.{prec}f}'.format(b, prec = precision).replace('-','').split('.')
    
    #on génére un nombre aléatoire qui sera l'endroit oü l'on va couper les 2 nombres et les croiser
    max_taille =  len(a_entiere) if len(a_entiere) <= len(b_entiere) else len(b_entiere)
    value = max_taille + precision - abs(int(random_number(0, precision + max_taille)))
    enfant1 = ""
    enfant2 = ""
    
    if value < precision:
        enfant1 = float(".".join([a_entiere,a_deci[:precision-value] + b_deci[:value]])) * (-1 if a < 0 else 1)
        enfant2 = float(".".join([b_entiere,b_deci[:precision-value]+ a_deci[:value]])) * (-1 if b < 0 else 1)
    elif value == precision:
        enfant1 = float(".".join([a_entiere,b_deci])) *(-1 if a < 0 else 1)
        enfant2 = float(".".join([b_entiere,a_deci])) *(-1 if b < 0 else 1)
    else:
        enfant1 = float(".".join([a_entiere[:len(a_entiere) - (value - precision)] + b_entiere[(value - precision):],b_deci])) *(-1 if a < 0 else 1)
        enfant2 = float(".".join([b_entiere[:len(b_entiere) - (value - precision)] + a_entiere[(value - precision):],a_deci])) *(-1 if b < 0 else 1)
    
    return enfant1, enfant2 

#test rapide pour comparer 2 individus (içi 2 meilleurs : anciens et nouveau)
def best_select(best_new_x,best_old_x,best_new_y,best_old_y):
    
    best_temp_x = best_new_x if best_new_x.get_erreur() < best_old_x.get_erreur() else best_old_x
    best_temp_y = best_new_y if best_new_y.get_erreur() < best_old_y.get_erreur() else best_old_y
    
    return best_temp_x, best_temp_y

def cross_tab(tab_x_old,generation,index):
    #on choisit alétoirement des individus à croisser (pas tomber dans des minimums locaux)
    tab_x = [ele for ele in tab_x_old if random_number(0,1,True) < pourcentage_select_croissement ]
    cross_x = []
    
    #va servir à changer les individus croisser ex : 1er génération 1 - 2 (croisées) 2e génération 1 - 3.....
    if tab_x is not None and len(tab_x) >= 2:
        index_switch_x = generation%(len(tab_x)//2)
        index_switch_x = 1 if index_switch_x == 0 else index_switch_x
        for i in range (0,(len(tab_x)-1)//2,2):
            cross_x += Individu.croisement(tab_x[i],tab_x[i+index_switch_x],index)

    return cross_x

#fonction pour avoir des valeurs alétoires soit d'une loi normal soit uniforme
def random_number(a = 0, b = 1, normal = False):
    if normal:
        return np.random.normal(a, b, 1)[0]
    return random.uniform(a-b, a+b)

def SolutionsPossibles(tab,nbpop,max_generation):
    #dans notre cas pas de lien de dépendance direct entre x et y (en tous cas pas explicité dans le sujet)
    #pas de lien entre les parametres des 2 equations sinon j'aurai réunis les 2
    pop_x = Individu.create_rand_pop(nbpop,1)
    pop_y = Individu.create_rand_pop(nbpop,2)
    old_pop_x = pop_x
    old_pop_y = pop_y
    
    #on initialise
    best_old_x = Individu(1)
    best_old_y = Individu(2)
    
    #va servir à afficher les vrais valeurs des (x,y)
    real_x = [i[1] for i in dataset]
    real_y = [i[2] for i in dataset]
    
    generation = 1
    
    #generation : génération et generation_max = nombre maximun de génération
    while generation <= max_generation:
        
        #on trie la population en fonction du fitness
        evaluation_x = Individu.evaluate(old_pop_x)
        evaluation_y = Individu.evaluate(old_pop_y)
        
        #on selectionne la partie meilleur et pire
        select1_x, select2_x = Individu.selection(evaluation_x,nombre_parent_pop,last)
        select1_y, select2_y = Individu.selection(evaluation_y,nombre_parent_pop,last)
        
        #on croise la moitié 'meilleur'
        croises_x = cross_tab(select1_x,generation,1)
        croises_y = cross_tab(select1_y,generation,2)
        
        #on mutes la moitié 'pire'
        mutes_x = []
        mutes_y = []
        for x,y in zip(select2_x,select2_y):
            mutes_x.append(Individu.mutation(x))
            mutes_y.append(Individu.mutation(y))
        
        #on crée de nouvelles populations aléatoires (pas tomber dans des minimun locaux)
        newalea_x = Individu.create_rand_pop(new_pop_generation,1)
        newalea_y = Individu.create_rand_pop(new_pop_generation,2)

        pop_x = select1_x[:] + croises_x[:] + mutes_x[:] + newalea_x[:]
        pop_y = select1_y[:] + croises_y[:] + mutes_y[:] + newalea_y[:]

        best_new_x = min(pop_x, key = lambda x : x.get_erreur())
        best_new_y = min(pop_y, key = lambda x : x.get_erreur())
        
        #on test les meilleurs (le nouveau et l'ancien)
        best_old_x, best_old_y = best_select(best_new_x, best_old_x, best_new_y, best_old_y)
        #on test les le meilleur avec un random
        best_old_x, best_old_y = best_select(Individu(1), best_old_x, Individu(2), best_old_y)
        
        
        old_pop_x = pop_x
        old_pop_y = pop_y
        generation += 1
        
        #tous les dix générations on affiche l'avancement
        if(generation%10==0):
            print(f"\n------ Génération n°{generation}")
            print(",".join([f"(p{i} : {j})" for i,j in zip(range(1,number_opti+1),best_old_x.get_val())]))
            print(f"(margine error) : {round(best_old_x.get_erreur(),4)}")
            print(",".join([f"(p{i} : {j})" for i,j in zip(range(4,number_opti+4),best_old_y.get_val())]))
            print(f"(margine error) : {round(best_old_y.get_erreur(),4)}")

            t = np.linspace(0, 2*np.pi, 1000)
            x = best_old_x.get_val()[0] * np.sin(best_old_x.get_val()[1]*t+best_old_x.get_val()[2])
            y = best_old_y.get_val()[0] * np.sin(best_old_y.get_val()[1]*t+best_old_y.get_val()[2])
            plt.plot(x,y)
            plt.scatter(real_x,real_y,s=1,color='red')
            plt.show()
        
        #faire une fonctin last_test qui regarde les valeurs autour de la/ les n permieres solutions
    
    return best_old_x,best_old_y
# %% zone du main
if __name__ == '__main__' :
    #on récupère la data du fichier csv
    with open(r'position_sample.csv','r') as f:
        
      old_tab = [line.replace('\n','').split(';') for line in f]
      old_tab = old_tab[1:]
      tab = [list(map(float,lst)) for lst in old_tab]
      #on transmet les données à une variable (qui pourra être accéder par toutes les fonctions : voir haut page)
      dataset = tab

      nbpop = int(input("Nombre de population : "))
      max_generation = int(input("Nombre de génération : "))
      #nombre de parent selectionnés pour les croissements
      nombre_parent_pop = nbpop//2
      #nombre de 'mauvais' individu selectionnés pour les mutations
      last = nbpop//4
      #nombre d'individu généré aléatoirement à chaque génération
      new_pop_generation = nbpop//4
      
      start = time.process_time()
      
      best_old_x,best_old_y = SolutionsPossibles(tab,nbpop, max_generation)
      
      end = time.process_time()

      print(f"\nLe temps écoulé est de {round(end - start,2)} secondes...")
      
      