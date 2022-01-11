import sysv_ipc
import sys
import os
import sys
import tkinter
import threading

key = 300
keyjeu = 400
pid = os.getpid()


#def offres():
 #   while True:
  #      m, _ = mq.receive(type=int(str(pid) + 1))
   #     print(m.decode())


# We connect to the message queue
try:
    mq = sysv_ipc.MessageQueue(key)
except sysv_ipc.ExistentialError:
    print("The message queue you're trying to connect to doesn't exist.")
    sys.exit(1)

try:
    mqjeu = sysv_ipc.MessageQueue(keyjeu)
except sysv_ipc.ExistentialError:
    print("The message queue you're trying to connect to doesn't exist.")
    sys.exit(1)
#thread_offres = threading.Thread(target=offres)
# If we want to be connected to the game
while True:
    n = input("Voulez-vous jouer ? oui/non: ")
    if n.lower() == "oui":
        break
    elif n.lower() == "non":
        print("Merci au revoir !")
        sys.exit(1)
    else:
        print("Votre saisie n'est pas valide. Veuillez réessayer.")
mq.send(str(pid).encode(), type=1)
# To listen to the server's answer
# To see if we are accepted or no
while True:
    m, _ = mq.receive(type=pid)
    m = m.decode()
    if m == "Tu es accepté dans la partie. En attente d'autres joueurs...":
        print(m)
        break
    if m == "La partie est pleine":
        print(m)
        sys.exit(1)

# To get our hand
while True:
    m, _ = mqjeu.receive(type=pid)
    m = m.decode()
    if m[:3] == "Ton":
        print(m)
        break

while True:
    # To receive the choice msg
    m, t = mqjeu.receive(type=pid)
    m = m.decode()
    if m == "Que voulez vous faire? Faire une offre(F), en accepter une(A) ou faire sonner la sonnerie(S) ?":
        print(m)
        while True:
            msg = str(input("Saisir votre choix: "))
            if msg.capitalize() != "F" and msg.capitalize() != "A" and msg.capitalize() != "S":
                print("Votre saisie est incorrecte. Veuileez réessayer")
            else:
                # Send either F, A or S
                msg = msg.encode()
                mqjeu.send(msg, type=pid)
                while True:
                    # To receive either the answer from the make offer, the accept an offer or ring the bell
                    m, _ = mqjeu.receive(type=pid)
                    m = m.decode()
                    if m == "Vous ne pouvez pas faire plus d'une offre":
                        print(m)
                        break
                    elif m == "Quelles cartes voulez-vous proposer ? (Par exemple: Shoes Shoes)":
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
                        cartes = (str(cartes)).encode()
                        mqjeu.send(cartes, type=pid)
                        while True:
                            eff, _ = mqjeu.receive(type=pid)
                            print(eff.decode())
                            # s'il accepte une offre apres en avoir fait une
