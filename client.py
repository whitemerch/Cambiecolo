import sysv_ipc
import sys
import os
import sys
import tkinter
import threading

key=300
keyjeu=400

def offres():
    while True:
        m, _ = mq.receive(type=int(str(os.getpid())+1))
        print(m.decode())

#We connect to the message queue
try:
    mq = sysv_ipc.MessageQueue(key)
except sysv_ipc.ExistentialError:
    print("The message queue you're trying to connect to doesn't exist.")
    sys.exit(1)

try:
    mqjeu=sysv_ipc.MessageQueue(keyjeu)
except sysv_ipc.ExistentialError:
    print("The message queue you're trying to connect to doesn't exist.")
    sys.exit(1)
thread_offres = threading.thread(target=offres)
#If we want to be connected to the game
while True:
    n = input("Voulez-vous jouer ? oui/non: ")
    if n.lower() == "oui":
        break
    elif n.lower() == "non":
        print("Merci au revoir !")
        sys.exit(1)
    else:
        print("Votre saisie n'est pas valide. Veuillez réessayer.")
mq.send(str(os.getpid()).encode(), type=1)
#To listen to the server's answer
#Just to the connection
while True:
    m , t = mq.receive()
    if t == 2 :
        print(m.decode())
        break
    if t == 3:
        print(m.decode())
        sys.exit(1)

while True:
    #To receive the choice msg
    m , t = mqjeu.receive(type=os.getpid())
    m = m.decode()
    print(m)
    while True:
        msg = int(input("Saisir votre choix: "))
        if msg.capitalize() != "F" or msg.capitalize() != "A" or msg.capitalize() != "S":
            print("Votre saisie est incorrecte. Veuileez réessayer")
        else:
            break



