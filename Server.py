from multiprocessing.managers import BaseManager
import random
import sysv_ipc
import signal
import os
import sys
import threading

mains_i = {}
jeu = []
class MyManager(BaseManager): pass
MyManager.register('sm')
m = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
m.connect()
sm = m.sm()
state=0 #Dadem
n=0
key = 703
stop=True

def handler(sig, frame):
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
    print(sm.get_points())
    while True:
        suite = str(input("Do you want to continue ?(yes/no)"))
        if suite == "yes":
            print("Resume ...")
            run()
            break
        elif suite == "no":
            for pids in mains_i.keys():
                try:
                    os.kill(pids, signal.SIGTERM)
                except OSError:
                    pass
            print("Leaving")
            mq.remove()
            sys.exit(1)
        else:
            print("Your input is incorrect. Retry ")

#To banish the players that want to enter the game when it's full
def nomore():
    while True:
        try:
            pid, _ = mq.receive(type=1)
            pid = int(pid.decode())
            msg = "The game is full"
            mq.send(msg.encode(), type=pid)
            os.kill(pid, signal.SIGTERM)
            if stop:
                sys.exit(1)
        except sysv_ipc.ExistentialError:
            print("Message queue closed\n Leaving")
            break
        except UnboundLocalError:
            print("Bye Bye")
            break



def deck(n):
    global jeu
    jeu = []
    transports = ["Shoes", "Bike", "Train", "Car", "Airplane"]
    for j in transports[:n]:
        for _ in range(5):
            jeu.append(j)
    random.shuffle(jeu)
    return jeu


def run():
    global jeu
    global stop
    global state
    global n
    global mains_i

    jeu = []
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    stop=True
    if state==0:
        n = int(input("How many players will play: "))
        print("Waiting for other players...")
    jeu = deck(n)
    i = 0
    k = 0
    if state==0:
        mains_i = {}
        while i < n:
            pid, _ = mq.receive(type=1)
            pid = int(pid.decode())
            print(pid)  # DEBUG
            # Creating our dict of offers and availability which is empty at the beginning
            offres = sm.get_offers()
            offre_i = []
            sm.set_offers(offre_i, pid)
            sm.set_flag(True, pid)
            main = jeu[k:k + 5]
            mains_i[pid] = main
            msg = "You're connected. Waiting for other players..."
            msg = msg.encode()
            # Sending the pid of the server to each client so they have it they may need it to ring the bell
            mq.send(msg, type=pid)
            pid_server = str(os.getpid())
            pid_server = pid_server.encode()
            mq.send(pid_server, type=pid)
            i += 1
            k += 5
        for pid, list in mains_i.items():
            main = (' '.join(list)).encode()
            mq.send(main, type=pid)
        stop=False
        state+=1
        thread.start()
    else:
        offres = sm.get_offers()
        offre_i = []
        for pids in offres.keys():
            mq.send((' '.join(jeu[k:k + 5])).encode(), type=pids)
            k+=5
            sm.set_flag(True, pids)
            sm.set_offers(offre_i, pids)
        

    

    signal.signal(signal.SIGUSR2, handler)
    signal.signal(signal.SIGINT, handler)
    signal.pause()


if __name__ == "__main__":
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    points = sm.get_points()
    for pid in mains_i.keys():
        sm.set_points(0, pid)
    thread = threading.Thread(target=nomore)
    run()
