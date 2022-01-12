import sysv_ipc
import os
import sys
import signal

def bell(pid):
    bell.acquire_bell()
    if list.count(list[0]) == len(list):
        os.kill(ppid,signal.SIGUSR4)
        print("Vous avez gagné")
    bell.release_bell()


key = 300
# Creation of our message queue
try:
    mq = sysv_ipc.MessageQueue(key)
except sysv_ipc.ExistentialError:
    print("The message queue you're trying to connect doesn't exist.")
    sys.exit(1)

if __name__ == "__main__":
    pid = os.getpid()
    while True:
        connection = str(input("Do you want to play?(yes/no"))
        if connection == "yes":
            print("Connecting...")
            break
        elif connection == "no":
            print("Leaving")
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