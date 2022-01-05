import pygame
from pygame.locals import *
import pygame_textinput
from multiprocessing import Lock
import random
import threading
import sysv_ipc
import os

keyConnect = 300

connexions = sysv_ipc.MessageQueue(keyConnect, sysv_ipc.IPC_CREAT)

#pygame.init()
#fenetre=pygame.display.set_mode((612,357), RESIZABLE)
#pygame.display.set_caption("Joueur")
#fond=pygame.image.load('background.jpg').convert()
#fenetre.blit(fond, (0,0))
#pygame.display.flip()
#continuer = 1
#while continuer:
    #for event in pygame.event.get():   
        #if event.type == QUIT:     
            #continuer = 0  

class Joueur():
    def __init__(self,identifiant, main, voyant):
        self.identifiant=identifiant
        self.main=main
        self.voyant=voyant
    def enlever_main(self, donne):
        for i in donne:
            self.main.remove(i)
    def ajouter_main(self, recu):
        for i in recu:
            self.main.append(i)

class Carte:
    def __init__(self,t):
        self.transport=t
    def __str__(self):
        return self.transport

#k depends on the number of player there. It's a variable that we whould get once everyone is connected
def deck(k):
    deck=[]
    transports=["Shoes","Bike","Train", "Car", "Airplane"]
    for j in transports[:k]:
        for _ in range(5):
            deck.append(Carte(j))
    return deck

def shuffle(deck):
    random.shuffle(deck)
    return deck

def jeu(joueur):
    if gagner(joueur.main)==True:
            print("Vous avez gagné")
    else:
        print("Vous n'avez pas gagné. Mytho")
    
    
def faireoffre(a,joueur):
    offres[joueur.identifiant[6]]=a

def retireroffre(joueur):
    try:
        del offres[joueur.identifiant[6]]
    except KeyError:
        print("Vous n'avez pas fait d'offres")

def gagner(list):
    gagner=False
    if list.count(list[0])==len(list):
        gagner=True
    return gagner


if __name__=="__main__":
    with () as manager:
        offres=manager.dict() #Nos offres sont contenues dans un dictionnaire dans le processus principal modifiable par les process
        joueurs=manager.list()
        nb=int(input("nbr de joueurs: "))
        deck=shuffle(deck(nb))
        k=0
        mains={}
        for i in range(1,6):
            mains[i]=deck[k:k+5]
            k+=5
        #mains={1:[Shoes, Airplane, Shoes, Bike, Airplane], 2:[...]...}
        j1=Joueur("joueur1", mains[1], 1)

        j2=Joueur("joueur2", mains[2], 1)

        j3=Joueur("joueur3", mains[3], 1)

        j4=Joueur("joueur4", mains[4], 1)

        j5=Joueur("joueur5", mains[5], 1)

        joueurs.extend([j1,j2,j3,j4,j5])

