import pygame
from pygame.locals import *
import pygame_textinput

from multiprocessing import Process, Queue, Lock, Manager
import random

queue=Queue()
mutex=Lock()

class Joueur():
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

def jeu(joueur):
    pass

def faireoffre(list,joueur):
    offres[joueur.identifiant[6]]=list

def retireroffre(joueur):
    joueur.main.append(offres[joueur.identifiant[6]])
    del offres[joueur.identifiant[6]]



def gagner(list):
    gagner=False
    if list.count(list[0])==len(list):
        gagner=True
    return gagner


if __name__=="__main__":
    with Manager() as manager:
        offres=manager.dict() #Nos offres sont contenues dans un dictionnaire dans le processus principal modifiable par les process
        nb=int(input("nbr de joueurs: "))
        deck=shuffle(deck(nb))
        k=0
        mains={}
        for i in range(1,6):
            mains[i]=deck[k:k+5]
            k+=5
        #mains={1:[Shoes, Airplane, Shoes, Bike, Airplane], 2:[...]...}
        j1=Joueur("joueur1", mains[1])
        p1=Process(target=jeu,args=(j1,))

        j2=Joueur("joueur2", mains[2])
        p2=Process(target=jeu,args=(j2,))

        j3=Joueur("joueur3", mains[3])
        p3=Process(target=jeu,args=(j3,))

        j4=Joueur("joueur4", mains[4])
        p4=Process(target=jeu,args=(j4,))

        j5=Joueur("joueur5", mains[5])
        p5=Process(target=jeu,args=(j1,))


        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()

        

        
        


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