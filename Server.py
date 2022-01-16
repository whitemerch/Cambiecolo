from multiprocessing.managers import BaseManager
import random
import sysv_ipc
import signal
import os
import sys


class MyManager(BaseManager): pass
MyManager.register('sm')
m = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
m.connect()
sm=m.sm()

key = 703
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)


def handler(sig, frame):
    if sig == signal.SIGUSR2:
        for pid in mains_i.keys():
            os.kill(pid, signal.SIGUSR2)
    print("La partie est terminée")
    mq.remove()
    sys.exit(1)


def deck(n):
    deck = []
    transports = ["Shoes", "Bike", "Train", "Car", "Airplane"]
    for j in transports[:n]:
        for _ in range(5):
            deck.append(j)
    random.shuffle(deck)
    return deck


if __name__ == "__main__":
    n = int(input("How many players will play: "))
    deck = deck(n)
    mains_i = {}
    i = 0
    k = 0
    while i < n:
        print(os.getpid())           #DEBUG
        pid, _ = mq.receive(type=1)
        pid = int(pid.decode())
        print(pid)                   #DEBUG

        # Creating our dict of offers and availability which is empty at the beginning
        offres = sm.get_offers()
        offre_i=[]
        sm.set_offers(offre_i, pid)

        sm.set_flag(True, pid)

        main = deck[k:k + 5]
        mains_i[pid] = main
        msg = "You're connected. Waiting for other players..."
        msg = msg.encode()
        #Sending the pid of the server to each client so they have it they may need it to ring the bell
        mq.send(msg, type=pid)
        pid_server=str(os.getpid())
        pid_server=pid_server.encode()
        mq.send(pid_server, type=pid)
        i += 1
        k += 5

    for pid, list in mains_i.items():
        main = (' '.join(map(str, list))).encode()
        mq.send(main, type=pid)


    test=sm.get_offers()
    print(test)
    signal.signal(signal.SIGUSR2, handler)
    signal.pause()
#Fermer les msgs queues
#Continuer la partie
#Faire dict de scores
