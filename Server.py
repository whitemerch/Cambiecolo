from multiprocessing.managers import BaseManager
import random
import sysv_ipc
import signal
import os
import sys
import threading

mains_i = {}
jeu = []

mains_i = {}
jeu = []

class MyManager(BaseManager): pass
MyManager.register('sm')
m = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
m.connect()
sm=m.sm()

<<<<<<< HEAD

MyManager.register('sm')
m = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
m.connect()
sm = m.sm()
=======
key = 703
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc

key = 703
stop=True

def handler(sig, frame):
<<<<<<< HEAD
    global stop
    if sig == signal.SIGINT:
        stop=True
        print("The game has been interrupted ")
        for pids in mains_i.keys():
            try:
                os.kill(pids, signal.SIGTERM)
            except OSError:
                pass
        print("Leaving")
        mq.remove()
        sys.exit(1)
    if sig == signal.SIGUSR2:
        for pid in mains_i.keys():
            os.kill(pid, signal.SIGUSR2)
    print("The game is finished")
    print("This is the points shart")
=======
    if sig == signal.SIGUSR2:
        for pid in mains_i.keys():
            os.kill(pid, signal.SIGUSR2)
    print("La partie est terminée")
    print("voici le tableau des points")
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
    print(sm.get_points())
    while True:
        suite = str(input("Do you want to continue ?(yes/no)"))
        if suite == "yes":
            print("Resume ...")
            run()
            break
        elif suite == "no":
<<<<<<< HEAD
            for pids in mains_i.keys():
                try:
                    os.kill(pids, signal.SIGTERM)
                except OSError:
                    pass
=======
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
            print("Leaving")
            mq.remove()
            sys.exit(1)
        else:
            print("Your input is incorrect. Retry ")

#To banish the players that want to enter the game when it's full
def nomore():
    while True:
        pid, _ = mq.receive(type=1)
        pid = int(pid.decode())
        msg = "The game is full"
        mq.send(msg.encode(), type=pid)
        os.kill(pid, signal.SIGTERM)
        if stop:
            sys.exit(1)

<<<<<<< HEAD

=======
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
def deck(n):
    global jeu
    jeu = []
    transports = ["Shoes", "Bike", "Train", "Car", "Airplane"]
    for j in transports[:n]:
        for _ in range(5):
            jeu.append(j)
    random.shuffle(jeu)
    return jeu
<<<<<<< HEAD


def run():
    global jeu
    global stop
    stop=True
    n = int(input("How many players will play: "))
    print("Waiting for other players...")
=======

def run():
    global jeu
    n = int(input("How many players will play: "))
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
    jeu = deck(n)
    global mains_i
    mains_i = {}
    i = 0
    k = 0
    while i < n:
        print(os.getpid())           #DEBUG
        pid, _ = mq.receive(type=1)
        pid = int(pid.decode())
<<<<<<< HEAD
        print(pid)  # DEBUG

        # Creating our dict of offers and availability which is empty at the beginning
        offres = sm.get_offers()
        offre_i = []
=======
        print(pid)                   #DEBUG

        # Creating our dict of offers and availability which is empty at the beginning
        offres = sm.get_offers()
        offre_i=[]
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
        sm.set_offers(offre_i, pid)

        sm.set_flag(True, pid)

        main = jeu[k:k + 5]
        mains_i[pid] = main
        msg = "You're connected. Waiting for other players..."
        msg = msg.encode()
        # Sending the pid of the server to each client so they have it they may need it to ring the bell
        mq.send(msg, type=pid)
<<<<<<< HEAD
        pid_server = str(os.getpid())
        pid_server = pid_server.encode()
        mq.send(pid_server, type=pid)
        i += 1
        k += 5
    stop=False
    thread.start()
=======
        pid_server=str(os.getpid())
        pid_server=pid_server.encode()
        mq.send(pid_server, type=pid)
        i += 1
        k += 5

>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
    for pid, list in mains_i.items():
        main = (' '.join(map(str, list))).encode()
        mq.send(main, type=pid)

    signal.signal(signal.SIGUSR2, handler)
<<<<<<< HEAD
    signal.signal(signal.SIGINT, handler)
    signal.pause()
=======
    signal.pause()
#Fermer les msgs queues
#Continuer la partie
#Faire dict de scores

>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc


if __name__ == "__main__":
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
<<<<<<< HEAD
    points = sm.get_points()
    for pid in mains_i.keys():
        sm.set_points(0, pid)
    thread = threading.Thread(target=nomore)
=======
    points=sm.get_points()
    for pid in mains_i.keys():
        sm.set_points(0, pid)
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
    run()
