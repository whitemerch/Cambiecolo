import sysv_ipc
from multiprocessing import Manager
import threading
import random

key = 300
keyjeu = 400
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
mqjeu = sysv_ipc.MessageQueue(keyjeu, sysv_ipc.IPC_CREAT)
playing = True
bell_lock = threading.Lock()

def deck():
    deck = []
    l=[]
    transports = ["Shoes", "Bike", "Train", "Car", "Airplane"]
    for j in transports :
        for _ in range(5):
            deck.append(j)
    random.shuffle(deck)
    return deck

def bell(pid):
    bell_lock.acquire()
    gagner = False
    list = mains[pid]
    if list.count(list[0]) == len(list):
        gagner = True
    bell_lock.release()
    return gagner

#sera invoqué chaque fois que quelqu'un update le dictionnaire offres
def offer_display():
    mes = str(offres).encode()
    mqjeu.send(mes, type=3)

def make_offer():
    pass

def accept_offer():
    pass

def jouer(pid):
    mes = "Votre main est: "+str(mains[pid])
    mes = mes.encode()
    mq.send(mes, type=pid)
    while playing:
        mes = "Que voulez vous faire? Faire une offre(F) ou en accepter une offre(A)"




def connection(n):
    joueurs = 0
    cartes = deck()
    k = 0
    while True:
        pid, _ = mq.receive(type=1)
        pid = int(pid.decode())
        if joueurs < n:
            joueurs += 1
            offres[pid] = []
            mains[pid] = cartes[k:k+5]
            scores[pid] = 0
            #locks[pid]=threading.Lock()
            dispo[pid] = True
            mes = "Ton identifiant est: " + str(pid)
            mes = mes.encode()
            mq.send(mes, type=2)
            play = threading.Thread(target=jouer, args=(pid,))
            play.start()
        elif joueurs == n:
            print("Le jeu peut commencer")
            mes = "La partie est pleine"
            mes = mes.encode()
            mq.send(mes, type=3)
            break
        k += 5


if __name__ == "__main__":
    with Manager() as manager:
        offres = manager.dict()
        mains = manager.dict()
        scores = manager.dict()
        locks = manager.dict()
        dispo = manager.dict()
        n = int(input("Combien de joueurs dans la partie : "))
        connection(n)
