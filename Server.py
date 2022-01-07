import sysv_ipc
from multiprocessing import Manager
import threading
import random

key = 300
keyjeu=400
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
mqjeu=sysv_ipc.MessageQueue(keyjeu, sysv_ipc.IPC_CREAT)
playing = True


def deck():
    deck = []
    l=[]
    transports = ["Shoes", "Bike", "Train", "Car", "Airplane"]
    for j in transports :
        for _ in range(5):
            deck.append(j)
    random.shuffle(deck)
    return deck

def jouer(pid):
    mes = "Votre main est: "+str(mains[pid])
    mes = mes.encode()
    mq.send(mes, type=pid)

def connection():
    joueurs = 0
    cartes = deck()
    k = 0
    while True:
        pid, _ = mq.receive(type=1)
        pid = int(pid.decode())
        if joueurs < 5:
            joueurs += 1
            offres[pid] = []
            mains[pid] = cartes[k:k+5]
            scores[pid] = 0
            mes = "Ton identifiant est: " + str(pid)
            mes = mes.encode()
            mq.send(mes, type=2)
            play = threading.Thread(target=jouer, args=(pid,))
            play.start()
        elif joueurs == 5:
            break
        k += 5


if __name__ == "__main__":
    with Manager() as manager:
        offres = manager.dict()
        mains = manager.dict()
        scores = manager.dict()
        connection = threading.Thread(target=connection)
        connection.start()
        connection.join()
