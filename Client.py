import sysv_ipc
import os
import sys
import signal
from multiprocessing.managers import BaseManager

<<<<<<< HEAD
main = []


class MyManager(BaseManager): pass


=======
main=[]

class MyManager(BaseManager): pass
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
MyManager.register('sm')
man = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
man.connect()
sm = man.sm()


def bell(pid):
    bell.acquire_bell()
    if list.count(list[0]) == len(list):
<<<<<<< HEAD
        os.kill(ppid, signal.SIGUSR2)
=======
        os.kill(ppid,signal.SIGUSR2)
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
        print("Vous avez gagné")
    bell.release_bell()

def handler(sig, frame):
    global main
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
        print("en attente de la main ...")
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
        print("Que voulez vous faire? Faire une offre(F), en accepter une(A) ou faire sonner la sonnerie(S) ?")


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
    global main
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

<<<<<<< HEAD
def handler(sig, frame):
    global main, ppid
    if sig == signal.SIGUSR1:
        print("quelqu'un veut échanger avec vous")
        offres = sm.get_offers()
        cartes = offres[pid]
        n = 0
        while n < len(current[pid]):
            for k in range(len(main)):
                if main[k] == cartes[0]:
                    main.pop(k)
                    n += 1
                    break
        msg = ""
        for q in range(len(cartes)):
            msg += cartes[q] + " "
        msg = msg.encode()
        mq.send(msg, type=1)
        n, _ = mq.receive(type=1)
        newcards = (n.decode()).split()
        for l in range(len(newcards)):
            main.append(newcards[l])
        print(main)
        print("Que voulez vous faire? Faire une offre(F), en accepter une(A) ou faire sonner la sonnerie(S) ?")


    elif sig == signal.SIGUSR2:
        print("quelqu'un a remporté cette manche")
        print("en attente de la main ...")
        m = str(pid)
        m = m.encode()
        mq.send(m, type=1)
        # To receive the msg that tells the player that he's connected
        m, _ = mq.receive(type=pid)
        m = m.decode()
        print(m)
        # We get the ppid of the server
        m, _ = mq.receive(type=pid)
        ppid = int(m.decode())
        # We get the hand of the player
        m, _ = mq.receive(type=pid)
        main = (m.decode()).split()
        print("Que voulez vous faire? Faire une offre(F), en accepter une(A) ou faire sonner la sonnerie(S) ?")
    elif sig == signal.SIGINT:
        os.kill(ppid, signal.SIGINT)  # I send sigint to the server if there is an interruption
    elif sig==signal.SIGTERM:
        print("The game has been interrupted")


def valide(list, main):
    n = 0
    for k in range(len(main)):
        if main[k] == list[0]:
            n += 1
    if len(list) > n:
        return False
    else:
        return True


def saisieCartes():
    global main
    while True:
        cartes_list = str(
            input("Quelles cartes voulez vous échanger ? (Mettez E pour revenir en arrière): "))
        if cartes_list == "E":
            print("On revient en arrière ")
            return False
        cartes_list = cartes_list.split()
        if not (
                all(item in ["Shoes", "Bike", "Train", "Car", "Airplane"] for item in cartes_list)):
            print("Your input is incorrect")
        elif len(cartes_list) > 3:
            print("You can't make an offer of more than 3 cards")
        # To see if what the user is writing is indeed the cards
        elif not (valide(cartes_list, main)):
            print("You don't have enough cards")
        elif not (len(set(cartes_list)) == 1):
            print("Your offer must be identical cards")
        else:
            return cartes_list


=======
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
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
<<<<<<< HEAD
        connection = str(input("Do you want to play?(yes/no) "))
=======
        connection = str(input("Do you want to play?(yes/no)"))
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
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
<<<<<<< HEAD
    msg1, _ = mq.receive(type=pid)
    msg1 = msg1.decode()
    print(msg1)
    # We get the ppid of the server
    ppid, _ = mq.receive(type=pid)
    ppid = int(ppid.decode())
    # We get the hand of the player
    main, _ = mq.receive(type=pid)
    main = (main.decode()).split()

    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    while True:
        while True:
            t = True
            print(main)
            print("What do you want to do ? Make an offer(F), accept one(A) or ring the bell(S) ?")
            msg = str(input("Make your choice: "))
            if msg.capitalize() != "F" and msg.capitalize() != "A" and msg.capitalize() != "S":
                print("Your input is incorrect. Retry !")
            else:
                # si la saisie est bonne
                if msg == "F":
                    current = sm.get_offers()
                    if current[pid]:
                        print("You can't make more than one offer")
                        break
                    cartes_list = saisieCartes()
                    if not cartes_list:
                        break
                    sm.acquire_lock()
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
                        cible = int(input("Avec qui voulez vous échanger ? (Mettez E pour revenir en arrière) "))
                        if cible == "E":
                            t == False
                            break
                        elif cible not in dispo.keys():
                            print("le joueur n'existe pas")
                        elif not (current[cible]):
                            print("Ce joueur n'a pas d'offres disponible")
                        elif dispo[cible] == False:
                            print("le joueur n'est pas disponible")
                        else:
                            break
                    if not t:
                        break
                    if not (len(current[pid]) == len(current[cible])):
                        cartes_list = saisieCartes()
                        if cartes_list == False:
                            break
                        while not (len(cartes_list) == len(current[cible])):
                            print("veuillez donner autant de cartes que le joueur")
                            cartes_list = saisieCartes()
                            if cartes_list == False:
                                break
                    if cartes_list == False:
                        break
                    sm.acquire_lock()
                    sm.set_offers(cartes_list, pid)
                    current = sm.get_offers()
                    dispo = sm.get_flag()
                    dispo[pid] = False
                    dispo[cible] = False
                    sm.release_lock()
                    # envoi d'un signal pour faire stopper la cible
                    os.kill(cible, signal.SIGUSR1)
                    # envoi des cartes avec mq ici
                    # reception (maj des cartes en main)
                    n = 0
                    while n < len(current[pid]):
                        for k in range(len(main)):
                            if main[k] == cartes_list[0]:
                                main.pop(k)
                                n += 1
                                break
                    n, _ = mq.receive()
                    newcards = (n.decode()).split()
                    for l in range(len(newcards)):
                        main.append(newcards[l])

                    offres = sm.get_offers()
                    cartes = offres[pid]
                    msg = ""
                    for q in range(len(cartes)):
                        msg += cartes[q] + " "
                    msg = msg.encode()
                    mq.send(msg, type=1)

                    sm.acquire_lock()
                    dispo = sm.get_flag()
                    dispo[pid] = True
                    dispo[cible] = True
                    current = sm.get_offers()
                    vide = []
                    sm.set_offers(vide, pid)
                    sm.set_offers(vide, cible)
                    sm.release_lock()
                    print(main)
                    break
                elif msg == "S":
                    if not (len(set(main)) == 1):
                        print("Vous n'avez pas des cartes identiques")
                    else:
                        points = sm.get_points()
                        if pid in points.keys():
                            point = points[pid]
                        else:
                            point = 0
                        if main[0] == "Shoes":
                            point += 1
                        elif main[0] == "Bike":
                            point += 2
                        elif main[0] == "Train":
                            point += 3
                        elif main[0] == "Car":
                            point += 4
                        elif main[0] == "Airplane":
                            point += 5
                        sm.acquire_lock()
                        sm.set_points(point, pid)
                        sm.release_lock()
                        os.kill(ppid, signal.SIGUSR2)
                    break
=======
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
                            while not(len(cartes_list)==len(current[cible])):
                                print("veuillez donner autant de cartes que le joueur")
                                cartes_list = saisieCartes()
                        sm.acquire_lock()
                        sm.set_offers(cartes_list, pid)
                        current = sm.get_offers()
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
                        if not(len(set(main)) == 1):
                            print("Vous n'avez pas que des cartes identiques")
                        else:
                            points=sm.get_points()
                            if pid in points.keys():
                                point=points[pid]
                            else:
                                point=0
                            if main[0]=="Shoes":
                                point+=1
                            elif main[0]=="Bike":
                                point+=2
                            elif main[0]=="Train":
                                point+=3
                            elif main[0]=="Car":
                                point+=4
                            elif main[0]=="Airplane":
                                point+=5
                            sm.acquire_lock()
                            sm.set_points(point, pid)
                            sm.release_lock()
                            os.kill(ppid, signal.SIGUSR2)
                        break
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
