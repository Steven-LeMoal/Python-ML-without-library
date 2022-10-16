#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 17:29:02 2022

@author: steven
"""

from sys import maxsize
from copy import deepcopy
import time

#Variable utile
#state : 0 (rien); 1 (noir); 2 (blanc)
#score max
maxi = 100000000
memorie = dict()
#axes
axes = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1),(1, -1)], [(-1, -1), (1, 1)]]
#cours reconnaissable

#Classe pour le plateau
class Board(object):
    def __init__(self):
        self.board = [['r' for j in range(15)] for i in range(15)]
        self.x = -1
        self.y = -1
        self.state = 'r'
    
    def get_board(self):
        return self.board
    
    def get_state(self,x,y):
        return self.board[x][y]
    
    def set_state(self,x, y,state):
        self.board[x][y] = state
        self.x = x
        self.y = y
        self.state = state
        
    def Affichage(self):
        print("\t", end='')
        print('\t'.join([str(i + 1) for i in range(15)]))
        print('\n'.join(['\t'.join([str(Symbole(self.board[i][j])) if j != 0 else  str(i + 1) + "\t" +  str(Symbole(self.board[i][j]))for j in range(15)]) for i in range(15)]))
        
        
    #check les points dans la même direction
    def direction(self,x,y,x_D,y_D,joueur):
        n = 0
        #4 case autour
        for case in range(1,5):
            #on vérifie qu'on est bien sur le plateau
            if InBoard(x_D,y,case) or InBoard(x_D,y,case):
                break
            if self.board[x + y_D * case][y + x_D * case] == joueur:
                n += 1
            else:
                break
        return n
    
    def result(self):
        if self.gagne(self.state):
            return self.state
        else:
            return 'r'
    
    def gagne(self,joueur):        
        result = False
        for x in range(15):
            for y in range(15): 
                    if(y <= 10 and x <= 10):
                        result = all(self.board[x][y] == self.board[x + j][y + j] and self.board[x][y] == joueur for j in range(5))
                        if(result): return True
                    if(y <= 10 and x > 10):
                        result = all(self.board[x][y] == self.board[x][y+j] and self.board[x][y] == joueur for j in range(5))
                        if(result): return True
                    elif(x <= 10):
                        result = all(self.board[x][y] == self.board[x + j][y] and self.board[x][y] == joueur for j in range(5))
                        if(result): return True

        return False
    

class Joueur(object):
    def __init__(self,board,state,pfd):
        self.board = board
        self.state = state
        self.pfd = pfd
        self.x_pos = -1
        self.y_pos = -1
        
    def set_board(self,x,y,state):
        self.board.set_state(x,y,state)
    
    def PionConnecter(self,x,y,x_D,y_D,state):
        n = 0
        for case in range(4):
            if InBoard3(x_D,y,case + 1) or InBoard3(y_D,x,case + 1):
                break
            if self.board.get_board()[x + y_D * (case + 1)][y + x_D * (case + 1)] == state:
                n += 1
            else:
                break
        return n
        
    def Voisin(self,x,y,state):
        for direction in axes:
            for (x_D,y_D) in direction:
                if(InBoard2(x_D,y) or InBoard2(y_D,x)):
                    break
                if self.board.get_board()[x+y_D][y+x_D] != 'r':
                    return True
                
                if (InBoard2(x_D,y,True) or InBoard2(y_D,x,True)):
                    break
                if self.board.get_board()[x + y_D * 2][y + x_D * 2] != 'r':
                    return True
        return False
    
    def Aligner4(self,x,y,state):
       for direction in axes:
           n = 1
           for (x_D,y_D) in direction:
               n += self.PionConnecter(x, y, x_D, y_D, state)
               if n == 4:
                   return True
               n = 1
       return False
    
    def Aligner5(self,x,y,state):
        for direction in axes:
            n = 1
            for (x_D,y_D) in direction:
                n += self.PionConnecter(x, y, x_D, y_D, state)
                if n >= 5:
                    return True
                n = 1
        return False
    
    
    def AdversaireAligner5(self,state):
        for direction in axes:
            n = 1
            for x in range(15):
                for y in range(15):
                    for (x_D,y_D) in direction:
                        n += self.PionConnecter(x, y, x_D, y_D, state)
                        if n >= 5:
                            return True
                        n = 1
        return False
    
    
    def CoupsPossible(self):
        coups = []
        for x in range(15):
            for y in range(15):
                if self.board.get_board()[x][y] == 'r':
                    if self.Voisin(x, y, self.board.get_board()[x][y]):
                        state2 = 'b' if self.state == 'n' else 'n'
                        tourSuivant = Joueur(deepcopy(self.board), state2,self.pfd - 1)
                        tourSuivant.set_board(x, y,self.state)
                        coups.append((tourSuivant,x,y,self.PointScore(x,y)))
                        
        return list(sorted(coups, key =lambda x : x[3]))
 
    def ComputeScore(self,coups):
        total = 0
        for e in coups:
            #print(e)
            n = evaluer(e)
            total += n['n'] - n['b'] if self.state == 'n' else n['b'] - n['n']
            #print(total)
        return total

    
    #donne le score du board (minimax)
    def BoardScore(self):
        coups = []
        
        for x in range(15):
            for y in range(15):
                    if(y <= 10 and x <= 10):
                        coups.append([self.board.get_board()[x+i][y+i] for i in range(15-y if x < y else 15-x)])
                    elif(y <= 10 and x > 10):
                        coups.append([self.board.get_board()[x][y+i] for i in range(15-y)])
                    elif(x <= 10):
                        coups.append([self.board.get_board()[x+i][y] for i in range(15-x)])
        """
        for y in range(15):
            coups.append(self.board.get_board()[y])
            lignes = []
            for x in range(15):
                lignes.append(self.board.get_board()[x][y])
            coups.append(lignes)
        
        for a in range(1,11):
            diago_x = []
            diago_y = []
            
            for b in range(a,15):
                diago_x.append(self.board.get_board()[a][a-b])
                diago_x.append(self.board.get_board()[a-b][a])
            
            #a+3 car on part de a = 1 (15 - 4 : 11 (range))
            #on veut ici prendre des trajectoires en partant de la fin
            
            coups.append([self.board.get_board()[a+3][b- a+3 - 1] for b in range(a+3,-1,-1)])
            coups.append([self.board.get_board()[a+3][15*2 - (a+3+b) - 2] for b in range(15 - a + 3 - 1,15)])
            
            coups.append(diago_x)
            coups.append(diago_y)
            
        
        coups.append([self.board.get_board()[x][x] for x in range(15)])
        coups.append([self.board.get_board()[x][15 - x - 1] for x in range(15)])
        
        """
        return self.ComputeScore(list(filter(lambda x : x.count('r') != len(x),coups)))
            
        
    #donne le score d'un point
    def PointScore(self,a,b):
        #tableau rassemblant la droite associer à aux points
        coups = []
        
         
        for x in range(15):
            for y in range(15):
                    if(y <= 10 and x <= 10):
                        tab = []
                        test = False
                        for i in range(15-y if x < y else 15-x):
                            tab.append(self.board.get_board()[x+i][y+i])
                            if(x+i) == a and y + i == b:
                                test = True
                        if test:
                            coups .append(tab)
                    elif(y <= 10 and x > 10):
                        tab = []
                        test = False
                        for i in range(15-y):
                            tab.append(self.board.get_board()[x][y+i])
                            if x == a and y+i == b:
                                test = True
                        if test:
                            coups .append(tab)
                    elif(x <= 10):
                        tab = []
                        test = False
                        for i in range(15-x):
                            tab.append(self.board.get_board()[x+i][y])
                            if(x+i) == a and y == b:
                                test = True
                        if test:
                            coups .append(tab)
        
        #memorie[(a,b)] = result
        
        return self.ComputeScore(list(filter(lambda x : x.count('r') != len(x),coups)))

    
    def AlphaBeta(self,joueur,a = -maxi ,b = maxi):
        if joueur.pfd <= 0:
            return - joueur.BoardScore()
        #on choisit le nombre de coups
        for (tourSuivant,x,y,score) in joueur.CoupsPossible():
            hold = - self.AlphaBeta(tourSuivant,-b,-a)
            if hold > b:
                return b
            if hold > a:
                a = hold
                (joueur.x_pos,joueur.y_pos) = (x,y)
        return a
        
        
    def Tour1(self):
        self.board.set_state(7,7,self.state)
        return True
    
    def TourK(self):
        for x in range(0,15):
            for y in range(0,15):
                if self.board.get_board()[x][y] == 'r':
                    if self.Aligner5(x, y, self.state):
                        print("Aligner 5..")
                        self.board.set_state(x,y,self.state)
                        return True
                    if self.Voisin(x, y, self.board.get_board()[x][y]):
                        if self.Aligner4(x, y, self.state):
                            print("Aligner 4 possible..")
                            if self.AdversaireAligner5(self.state):
                                print("L'adversaire nous a mis en Aligner 5")
                            else:
                                self.board.set_state(x,y,self.state)
                                return True
        
        jA = Joueur(self.board,self.state,self.pfd)
        best = self.AlphaBeta(jA)
        print(best)
        (x,y) = (jA.x_pos,jA.y_pos)
        
        if not x is None and not y is None: 
            if self.board.get_board()[x][y] == 'r':
                print(f"({x + 1},{y + 1})")
                print("")
                self.board.set_state(x,y,self.state)
                return True


        return False
    
    def InputCoord(self):
        x = -1
        y = -1
        test = False
        
        while not test:
            while x < 1 or x > 15:
                x = int(input("Veuillez saisir la coordonnées x : "))
            
            while y < 1 or y > 15:
                y = int(input("Veuillez saisir la coordonnées y : "))
                
           
            
            if not x is None and not y is None: 
                x -= 1
                y -= 1
                if self.board.get_state(x,y) == 'r':
                    self.board.set_state(x,y,self.state)
                    break
                else:
                    x = -1
                    y = -1
                    print("Veuillez saisir une case vide")
        
        return True
        
#Fonction utile
#Fonction pour tester des projeter de coordonnées
#check si un point à 4 cases est sur le tableau

def InBoard3(direction,coord1,coord2):
    return direction != 0 and (coord1 + direction * coord2 < 0 or direction * coord2 + coord1 >= 15)
#check les voisins sur les 4 axes en vérifiant s'il sont sur le tableau
def InBoard2(direction,coord,test2d = False):
    if test2d:
        return direction != 0 and (coord + direction * 2 < 0 or coord + direction * 2 >= 15)
    else:
        return direction != 0 and (coord + direction < 0 or coord + direction >= 15)
#check les voisins sur les 4 axes en vérifiant s'il sont sur le tableau
def InBoard(direction, coord1, coord2):
    return direction != 0 and (coord1 * coord2 + direction < 0 or direction * coord2 + coord1 >= 15)


def evaluer(elements):
    score = {'b' : 0,'n' : 0}
    for a in elements:
        state = 'n'
        for i in range(2):
            n = PionConnecter2(a, state)
            add = 0 if elements.count(state) == 0 else 1
            score[state] += 10**n * add
            state = 'b'
            
    return score

def PionConnecter2(tab,state):
    n = 0
    for i in range(1, len(tab)):
        if tab[i-1] == tab[i] and tab[i] == state:
            n+=1
    return n

#avec board1 > board2
def test_pattern(board1,board2):
    for x in range((len(board1)-len(board2))+ 1):
        for y in range(len(board2)):
            if board1[x+y] == board2[y]:
                return True
            else:
                break
    return False

def Symbole(ele):
    if ele == 'n':
        return 'x'
    elif ele == 'b':
       return 'o'
    else:
       return '-'
    

def Inputia():
        x = -1
        y = -1
        
        while x < 0 or x > 1:
            x = int(input("Ia contre Ia ? 0 (oui) 1 (non) : "))
        
        print()
        
        while y < 0 or y > 1:
            y = int(input("Ia joue en premier ? 0 (oui) 1 (non) : "))
        
        print()
        
        if(x == 0):
            return True,True
        if(x==1 and y==0):
            return True,False
        if(x==1 and y == 1):
            return False,True

if __name__ == '__main__': 
    jeu = Board()
    jeu.Affichage()
    print()
    
    
    j1_ia , j2_ia = Inputia()
    pfd = 0

    while pfd < 1:
        pfd = int(input("Difficulté de l'IA (de 1 à ... : recommandé 2 ou 3) : "))
        
    print()

    joueur1 = Joueur(jeu,'n',pfd)
    joueur2 = Joueur(jeu,'b',pfd)
    
    result = 'r'
    

    joueur1.Tour1()
    resultat = jeu.result()        
    jeu.Affichage()
    print()
    
    nbTour = 0
    
    while nbTour <= 60:
        nbTour += 1
        #ia vs ia
        if j2_ia and j1_ia:
            joueur2.TourK()
            result = jeu.result()
            jeu.Affichage()
            time.sleep(2)
            print()
            
            
            if result != 'r':
                print(result + "Win")
                break
            if j1_ia:
                joueur1.TourK()
                result = jeu.result()
                jeu.Affichage()
                time.sleep(2)
                print()

                if result != 'r':
                    print(result + "Win")
                    break
            else:
                jeu.Affichage()
                print()
        else:
            #joueur vs ia
            if j2_ia:
                joueur2.TourK()
                result = jeu.result()
                jeu.Affichage()
            else:
                joueur2.InputCoord()
                print()
                result = jeu.result()
                jeu.Affichage()
            
            if result != 'r':
                print(result + "Win")
                break
            
            print()
            
            if j1_ia:
                joueur1.TourK()
                result = jeu.result()
                jeu.Affichage()
            else:
                joueur1.InputCoord()
                print()
                result = jeu.result()
                jeu.Affichage()
            
            if result != 'r':
                print(result + "Win")
                break
            
            print()
        
        
        
        
    
    