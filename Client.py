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
        offres=sm.get_offers()
        cartes=offres[pid]
        n=0
        while n<len(current[pid]):
            for k in range (len(main)):
                if main[k]==cartes[0]:
                    main.pop(k)
                    n+=1
                    break
        msg=""
        for q in range (len(cartes)):
            msg +=cartes[q]+" "
        msg=msg.encode()
        mq.send(msg, type=1)
        n, _=mq.receive(type=1)
        newcards = (n.decode()).split()
        for l in range(len(newcards)):
                main.append(newcards[l])
        print(main)
        print("Que voulez vous faire? Faire une offre(F), en accepter une(A) ou faire sonner la sonnerie(S) ?")


    elif sig==signal.SIGUSR2:
        print("quelqu'un a remporté cette manche")
        sys.exit(1)


def valide (list, main):
    n=0
    for k in range(len(main)):
        if main[k]==list[0]:
            n+=1
    if len(list)>n:
        return False
    else:
        return True


def saisieCartes():
    while True:
        print(main)
        cartes = str(input("quelles cartes voulez vous échanger ? "))
        cartes_list = cartes.split()
        if len(cartes_list) > 3:
            print("Vous ne pouvez pas faire une offre de plus de 3 cartes")
        # To see if what the user is writing is indeed the cards
        elif not(valide(cartes_list, main)):
            print("vous n'avez pas assez de ces cartes")
        elif not(all(item in ["Shoes", "Bike", "Train", "Car", "Airplane"] for item in cartes_list)):
            print("Votre saisie est incorrecte")
        elif not(len(set(cartes_list)) == 1):
            print("Votre proposition doit comporter des cartes identiques")
        else:
            return cartes_list
            break

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
        while True:
            print("Que voulez vous faire? Faire une offre(F), en accepter une(A) ou faire sonner la sonnerie(S) ?")
            msg = str(input("Saisir votre choix: "))
            if msg.capitalize() != "F" and msg.capitalize() != "A" and msg.capitalize() != "S":
                print("Votre saisie est incorrecte. Veuileez réessayer")
            else:
                while True:
                    # si la saisie est bonne
                    if msg == "F":
                        cartes_list = saisieCartes()
                        sm.acquire_lock()
                        current = sm.get_offers()
                        sm.set_offers(cartes_list, pid)
                        current = sm.get_offers()
                        print(current)
                        sm.release_lock()
                        break
                    elif msg == "A":
                        current = sm.get_offers()
                        print(current)
                        while True:
                            dispo = sm.get_flag()
                            print(dispo)
                            cible=int(input("Avec qui voulez vous échanger ?"))
                            if cible not in dispo.keys():
                                print("le joueur n'existe pas")
                            elif dispo[cible] == False:
                                print("le joueur n'est pas disponible")
                            else:
                                break
                        if not(len(current[pid])==len(current[cible])):
                            cartes_list = saisieCartes()
                        sm.acquire_lock()
                        dispo = sm.get_flag()
                        dispo[pid] = False
                        dispo[cible] = False
                        sm.release_lock()
                        #envoi d'un signal pour faire stopper la cible
                        os.kill(cible, signal.SIGUSR1)
                        #envoi des cartes avec mq ici
                        #reception (maj des cartes en main)
                        n=0
                        while n<len(current[pid]):
                            for k in range (len(main)):
                                if main[k]==cartes_list[0]:
                                    main.pop(k)
                                    n+=1
                                    break
                        n, _=mq.receive()
                        newcards=(n.decode()).split()
                        for l in range(len(newcards)):
                                main.append(newcards[l])

                        offres=sm.get_offers()
                        cartes=offres[pid]
                        msg=""
                        for q in range (len(cartes)):
                            msg +=cartes[q]+" "
                        msg=msg.encode()
                        mq.send(msg, type=1)


                        sm.acquire_lock()
                        dispo = sm.get_flag()
                        dispo[pid]=True
                        dispo[cible]=True
                        current = sm.get_offers()
                        vide=[]
                        sm.set_offers(vide, pid)
                        sm.set_offers(vide, cible)
                        sm.release_lock()
                        print(main)
                        break
                    elif msg =="S":
                        os.kill(ppid, signal.SIGUSR2)