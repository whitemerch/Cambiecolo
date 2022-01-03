import pygame
from pygame.locals import *
import pygame_textinput

from multiprocessing import Queue, Lock
import random


class Joueur:
    def __init__(self,identifiant,main):
        self.identifiant=identifiant
        self.main=main
    def enlever_main(self,main,donne):
        for i in donne:
            self.main.remove(i)
    def ajouter_main(self,main,recu):
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

def gagner(list):
    gagner=False
    if list.count(list[0])==len(list):
        gagner=True
    return gagner


if __name__=="__main__":
    
    nb=int(input("nbr de joueurs: "))
    deck=shuffle(deck(nb))


    #if gagner(list):
        #envoyer signaux a tous les clients

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