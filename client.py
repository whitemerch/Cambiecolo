import sysv_ipc
import sys
import os

key=300

#We connect to the message queue
try:
    mq = sysv_ipc.MessageQueue(key)
except sysv_ipc.ExistentialError:
    print("The message queue you're trying to connect to doesn't exist.")
    sys.exit(1)

#If we want to be connected to the game
while True:
    n = input("Voulez-vous jouer ? oui/non: ")
    if n == "oui":
        break
    else:
        print("Votre saisie n'est pas valide. Veuillez réessayer.")
mq.send(str(os.getpid()).encode(), type=1)
#To listen to the server's answer
while True:
    m , t = mq.receive()
    if t == 2 :
        print(m.decode())
        break
    if t == 3:
        print(m.decode())
        sys.exit(1)

while True:
    m , t = mq.receive(type=os.getpid())
    m = m.decode()
    print(m)


