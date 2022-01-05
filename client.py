import sysv_ipc
import sys
import os

key=300
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
#recevoir l'objet joueur
try:
    mq = sysv_ipc.MessageQueue(key)
except sysv_ipc.ExistentialError:
    print("Cannot connect to message queue", key, ", terminating.")
    sys.exit(1)
while True:
  n=input("Voulez vous jouer ? oui/non")
  if n=="oui":
    break
mq.send(os.pid(),type=2)
while True:
    if joueur.voyant==1:
        m,_=mq.receive(type=(os.pid()))
        m=m.decode()
        if m=="done":
            joueur.voyant=0
        else:
            print(m)
    else:
        tosend=input("\n")
        msg=tosend.encode()
        mq.send(msg,type=5)
        joueur.voyant=1
        
    print(m)
