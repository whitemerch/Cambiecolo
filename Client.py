import sysv_ipc
import os
import sys
import signal
from multiprocessing.managers import BaseManager

class MyManager(BaseManager): pass
MyManager.register('sm')
man = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
man.connect()
sm = man.sm()


def bell(pid):
    bell.acquire_bell()
    if list.count(list[0]) == len(list):
        os.kill(ppid,signal.SIGUSR2)
        print("Vous avez gagné")
    bell.release_bell()

def handler(sig, frame):
    if sig==signal.SIGUSR1:
        print("quelqu'un veut échanger avec vous")
    elif sig==signal.SIGUSR2:
        print("quelqu'un a remporté cette manche")
        sys.exit(1)


def valide (list, pid):
    c1, c2 = Counter(list), Counter(mains[pid])
    for k, n in c1.items():
        if n>c2[k]:
            return False



key = 703
# Creation of our message queue
try:
    mq = sysv_ipc.MessageQueue(key)
except sysv_ipc.ExistentialError:
    print("The message queue you're trying to connect doesn't exist.")
    sys.exit(1)

if __name__ == "__main__":
    pid = os.getpid()
    while True:
        connection = str(input("Do you want to play?(yes/no)"))
        if connection == "yes":
            print("Connecting...")
            break
        elif connection == "no":
            print("Leaving")
            sys.exit(1)
        else:
            print("Your input is incorrect. Retry ")
    m = str(pid)
    m = m.encode()
    mq.send(m, type=1)
    # To receive the msg that tells the player that he's connected
    m, _ = mq.receive(type=pid)
    m = m.decode()
    print(m)
    #We get the ppid of the server
    m, _ = mq.receive(type=pid)
    ppid = int(m.decode())
    #We get the hand of the player
    m, _ = mq.receive(type=pid)
    main=(m.decode()).split()

    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)

    while True:
        print("Que voulez vous faire? Faire une offre(F), en accepter une(A) ou faire sonner la sonnerie(S) ?")
        print(m)
        while True:
            msg = str(input("Saisir votre choix: "))
            if msg.capitalize() != "F" and msg.capitalize() != "A" and msg.capitalize() != "S":
                print("Votre saisie est incorrecte. Veuileez réessayer")
            else:
                while True:
                    # si la saisie est bonne
                    if msg == "F":
                        while True:
                            cartes = str(input(m))
                            cartes_list = cartes.split()
                            if len(cartes_list) > 3:
                                print("Vous ne pouvez pas faire une offre de plus de 3 cartes")
                            # To see if what the user is writing is indeed the cards
                            elif not(all(item in ["Shoes", "Bike", "Train", "Car", "Airplane"] for item in cartes_list)):
                                print("Votre saisie est incorrecte")
                            elif not(len(set(cartes_list)) == 1):
                                print("Votre proposition doit comporter des cartes identiques")
                            else:
                                break
                        sm.acquire_lock()
                        current = sm.get_offers()
                        current [pid] = cartes
                        sm.set_offers(current, pid)
                        print(current)
                        sm.release_lock()
                    elif msg == "A":
                        current = sm.get_offers()
                        print(current)
                        while True:
                            dispo = sm.get_flag()
                            cible=str(input("Avec qui voulez vous échanger ?"))
                            if cible not in current.keys():
                                print("le joueur n'existe pas")
                            elif dispo[cible] == False:
                                print("le joueur n'est pas disponible")
                            else:
                                break
                        sm.acquire_lock()
                        dispo = sm.get_flag()
                        dispo[pid] = False
                        dispo[cible] = False
                        sm.release_lock()
                        #envoi d'un signal pour faire stopper la cible
                        os.kill(cible, SIGURS2)
                        #envoi des cartes avec mq ici
                        #puis reception (maj des cartes en main)
                        sm = acquire_lock()
                        dispo = sm.get_flag()
                        dispo[pid]=True
                        dispo[cible]=True
                        current = sm.get_offers()
                        current[pid]=[]
                        current[cible]=[]
                        sm.release_lock()
                    elif msg =="S":
                        print("babar")
