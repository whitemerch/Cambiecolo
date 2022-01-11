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
offres_lock = threading.Lock()

def deck():
    deck = []
    transports = ["Shoes", "Bike", "Train", "Car", "Airplane"]
    for j in transports[:n] :
        for _ in range(5):
            deck.append(j)
    random.shuffle(deck)
    return deck

def bell(pid):
    bell_lock.acquire()
    list = mains[pid]
    if list.count(list[0]) == len(list):
        for i in continuer:
            continuer[i]=False
            win = "L'utilisateur"+str(pid)+" a gagné."
            mq.send(win.encode(), type=i)
    bell_lock.release()

#sera invoque chaque fois que quelqu'un update le dictionnaire offres
def offer_display():
    mes = str(offres).encode()
    for pid in players:
        mqjeu.send(mes, type=int(str(pid)+1))

def make_offer(pid, list):
    offres_lock.acquire()
    offres[pid]=list
    offres_lock.release()
    offer_display()
    pass

def accept_offer():
    offres_lock.acquire()
    offres_lock.release()
    offer_display()
    pass

def valide(list, pid):
    #It transforms both lists into a set to see if the cards given by the player are really in his hand
    return (set(list)).issubset(set(mains[pid]))

def jouer(pid):
    while playing:
        if not continuer[pid]:
            break
        mes = "Votre main est: " + str(mains[pid])
        mes = mes.encode()
        mqjeu.send(mes, type=pid)
        mes = "Que voulez vous faire? Faire une offre(F), en accepter une(A) ou faire sonner la sonnerie(S) ?"
        mes = mes.encode()
        mqjeu.send(mes, type=pid)
        #The answer of the choice
        while True:
            m,_= mqjeu.receive(type=pid)
            m = m.decode()
            if m == "F":
                if not offres[pid]:
                    msg="Vous ne pouvez pas faire plus d'une offre"
                    msg = msg.encode()
                    mqjeu.send(msg, type=pid)
                else:
                    msg = "Quelles cartes voulez-vous proposer ?"
                    msg=msg.encode()
                    mqjeu.send(msg, type=pid)
                    echange, _ = mqjeu.receive(type=pid)
                    echange = echange.decode()
                    if valide(echange,pid)==True:
                        make_offer(pid, echange)
                    else:
                        msg = "Vous n'avez pas les cartes que vous pretendez avoir"
                        msg = msg.encode()
                        mqjeu.send(msg, type=pid)
            #elif m =="A":

            else:
                bell(pid)


def connection():
    cartes = deck()
    k = 0
    while True:
        pid, _ = mq.receive(type=1)
        pid = int(pid.decode())
        if len(players) < n:
            players.append(pid)
            offres[pid] = []
            mains[pid] = cartes[k:k+5]
            scores[pid] = 0
            dispo[pid] = True
            continuer[pid] = True
            mes = "Ton identifiant est: " + str(pid)
            mes = mes.encode()
            mq.send(mes, type=2)
            play = threading.Thread(target=jouer, args=(pid,))
            play.start()
        elif len(players) >= n:
            mes = "La partie est pleine"
            mes = mes.encode()
            mq.send(mes, type=3)
        k += 5


if __name__ == "__main__":
    with Manager() as manager:
        players =[]
        offres = manager.dict()
        mains = manager.dict()
        scores = manager.dict()
        dispo = manager.dict()
        continuer=manager.dict()
        n = int(input("Combien de joueurs dans la partie : "))
        connection = threading.Thread(target=connection)
        connection.start()
        connection.join()
