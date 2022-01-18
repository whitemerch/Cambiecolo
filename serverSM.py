from multiprocessing.managers import BaseManager as MyManager
import os
import sys
import random
import sysv_ipc
import signal
import time
import ascii_art
import threading 


key = 200
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
MyManager.register('sm')
m = MyManager(address=("127.255.255.254", 8888), authkey=b'abracadabra')
m.connect()
sm = m.sm()
hands_items = {} #hands of player (will be needed one time only)
deck=[] #deck of cards
needToStop=True
n=0 #nbr of players
games=0 #nbr of games played

def deckS(n): #Designating and Shuffling cards in deck
    global deck #deck() function has now acces to theglobal variable [String]deck
    deck = []
    transports = ["Shoes", "Bike", "Train", "Car", "Airplane"]
    for j in transports[:n]: #:n => for n different cards if there is n player
        for _ in range(5):
            deck.append(j)
    random.shuffle(deck)
    return deck

def game():
    global deck
    global hands_items
    global needToStop
    global n
    global games
    needToStop=True 
    deck=[]
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    if games==0:
        n = int(input("Number n of players:"))
    deck = deckS(n)
    hands_items = {}
    i, k = 0, 0
    if games==0:
        hands_items ={}
        while i < n: 
            pid, _ = mq.receive(type=1)
            pid = int(pid.decode()) #receiving pid of player
            offers = sm.get_offers() #Dictionnary type of offers
            offers_items=[]
            sm.set_offers(offers_items, pid) #{pid: []} starting an empty one
            sm.set_flag(True, pid)
            main = deck[k:k + 5]
            hands_items[pid] = main
            art=ascii_art.title()
            toSend = art+"\nWelcome Player "+str(pid)+"! \n You already know the rules, so no need to explain them again :p \n You're now waiting for your friends, at least if you have them."
            toSend = toSend.encode()
            #Sending the pid of the server to each client so they have it they may need it to ring the bell
            mq.send(toSend, type=pid)
            pid_server=str(os.getpid()) # will send its owns pid (ppid variable in client file)
            pid_server=pid_server.encode()
            mq.send(pid_server, type=pid)
            i,k=i+1,k+5
        for pid, list in hands_items.items():
            hand_pid = (' '.join(list)).encode() #send the initial hand for each client
            mq.send(hand_pid, type=pid)
        games+=1
        needToStop=False
        thread.start()
    else:
        offers = sm.get_offers() #Dictionnary type of offers
        offers_items=[]
        for pid in offers.keys():
            hand_pid = (' '.join(deck[k:k+5])).encode() #send the initial hand for each client
            mq.send(hand_pid, type=pid)
            k+=5
            sm.set_offers(offers_items, pid) #{pid: []} starting an empty one
            sm.set_flag(True, pid)
    signal.signal(signal.SIGUSR2, handler)
    signal.signal(signal.SIGINT, handler) 
    signal.pause() #pause and wait for a signal

#End signal handler (SIGUSR2)
def handler(sig, frame):
    global needToStop
    if sig == signal.SIGINT: 
        needToStop=True
        print("The game will be interrupted...")
        for pid in hands_items.keys():
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError:
                pass 
        mq.remove()
        sys.exit(1) 
    if sig == signal.SIGUSR2:
        for pid in hands_items.keys():
            os.kill(pid, signal.SIGUSR2) #send SIGUSR2 to process's pid
    print("THE GAME IS OOOOVER!") #Change print to mq.send
    print("Recovering Scores Table")
    waitingStyle()
    print("{USER : ACTUAL SCORE}")
    print(sm.get_points())
    while True:
        kp=input("Do you want to keep going? Put yes to play :) or anything to quit :(")
        if kp =="yes":
            waitingStyle()
            print("Welcome again!")
            game()
            break
        else:
            print(ascii_art.credits())
            print("See you soon!")
            for pid in hands_items.keys():
                try:
                    os.kill(pid, signal.SIGTERM)
                except OSError:
                    pass
            mq.remove() #Quiting and removing the message queue
            sys.exit(1)

#Stylistic waiting
def waitingStyle(): #to launch for moving points
    print("",end="")
    time.sleep(1) #do some work here...
    print("\r.  ",end="")
    time.sleep(1) #do some more work here...
    print("\r.. ",end="")
    time.sleep(1) #do even more work...
    print("\r...",end="")
    time.sleep(1) #gratuitious amounts of work...


def listenAndBan(): 
    global needToStop
    while True:
        try:
            pid, _ = mq.receive(type=1)
            pid = int(pid.decode())
            toSend="NO MORE PLACES"
            mq.send(toSend.encode(), type=pid)
            os.kill(pid,signal.SIGTERM)
            if needToStop:
                sys.exit(1)
        except sysv_ipc.ExistentialError :
            print("Closing Message Queue\nQuitting...")
            break
        except sysv_ipc.ExistentialError :
            print("See you soon")
            break

if __name__ == "__main__":
	mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
	pts=sm.get_points()
	for pid in hands_items.keys():
	        sm.set_points(0,pid)
	thread = threading.Thread(target=listenAndBan) 
	game() 
