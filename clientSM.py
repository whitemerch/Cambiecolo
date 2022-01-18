#!/usr/bin/env python3
import os
import sysv_ipc
import sys
from multiprocessing.managers import BaseManager as MyManager
import signal
import time


key = 200
try:
    mq = sysv_ipc.MessageQueue(key)
except sysv_ipc.ExistentialError:
    print("Cannot connect to message queue", key, ", terminating.")
    sys.exit(1)

hand=[] #global variable of hand of client
MyManager.register('sm')
m = MyManager(address=("127.255.255.254", 8888), authkey=b'abracadabra')
m.connect()
sm = m.sm()

def handler(sig, frame):
    global hand 
    global ppid
    if sig==signal.SIGUSR1:
        print("Knock Knock! Someone want to exchange cards with you!")
        offers=sm.get_offers()
        cards=offers[pid]
        n=0
        while n<len(currentOffers[pid]):
            for k in range (len(hand)):
                if hand[k]==cards[0]:
                    hand.pop(k)
                    n+=1
                    break
        toSend=""
        for v in range (len(cards)):
            toSend +=cards[v]+" "
        toSend=toSend.encode()
        mq.send(toSend, type=3)
        n, _=mq.receive(type=3)
        newCardsrcv = (n.decode()).split()
        for l in range(len(newCardsrcv)):
            hand.append(newCardsrcv[l])
        print(hand)
        print("What you can do now : \nDo an offer (by typingF)\nAccept an offer(A)\nTold everyone that the only winner here is YOU!(S)\nOr do nothing")
    elif sig==signal.SIGUSR2:
        print("Someone won, It's the end of a game!")
        print("Waiting for decision from server...")
        try:
            m, _ = mq.receive(type=pid)
        except sysv_ipc.Error:
            sys.exit(1)
        hand=(m.decode()).split()
        print(hand)
        print("What you can do now : \nDo an offer (by typingF)\nAccept an offer(A)\nTold everyone that the only winner here is YOU!(S)\nOr do nothing")
    elif sig==signal.SIGINT: 
        try:
            os.kill(ppid, signal.SIGINT)  # I send sigint to the server if there is an interruption
        except ProcessLookupError:
            sys.exit(1)
            pass
    elif sig==signal.SIGTERM:
        print("THE GAME HAS BEEN INTERRUPTED! DON'T WORRY, IT'S NOT YOUR FAULT.")
        sys.exit(1)


def valide (list, hand):
    n=0
    for k in range(len(hand)):
        if hand[k]==list[0]:
            n+=1
    if len(list)>n:
        return False
    else:
        return True


def cardsXchgChoice():
    global hand
    while True:
        cards_list = str(input("Choose the cards you want to exchange (eg. type :'Shoes' or 'Bike Bike') (A to go back): "))
        if cards_list == "A":
            print("You changed your mind!")
            return False
        cards_list = cards_list.split()
        if not (
                all(item in ["Shoes", "Bike", "Train", "Car", "Airplane"] for item in cards_list)):
            print("That's not a card from the game")
        elif len(cards_list) > 3:
            print("You're not allowed to offer more than 3 cards")
        # To see if what the user is writing is indeed the cards
        elif not (valide(cards_list, hand)):
            print("You don't have the cards you've chosen")
        elif not (len(set(cards_list)) == 1):
            print("The choosen cards needs to be similar")
        else:
            return cards_list

if __name__ == "__main__":
    pid = os.getpid()
    print("Hey! if you're here, that means you want play!\nBut just in case you changed your mind, let us know!")
    while True:
        connection = str(input("Do you really want to play? Type 'yes' to play and anything you want to quit"))
        if connection == "yes":
            print("Connecting...")
            break
        else:
            print("Quitting...")
            quit()
    m = str(pid)
    m = m.encode()
    mq.send(m, type=1)
    # To receive the toSend that tells the player that he's connected
    m, _ = mq.receive(type=pid)
    m = m.decode()
    print(m)
    #We get the ppid of the server
    m, _ = mq.receive(type=pid)
    ppid = int(m.decode())
    #We get the hand of the player
    m, _ = mq.receive(type=pid)
    hand=(m.decode()).split(' ')

    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    signal.signal(signal.SIGINT, handler) 
    signal.signal(signal.SIGTERM, handler)

    while True:
        while True:
            verif = True
            time.sleep(1)
            print(hand)
            print("What you can do now : \nDo an offer (by typing F)\nAccept an offer(A)\nTold everyone that the only winner here is YOU!(S)\nOr do nothing")
            msg = str(input("Your choice is: "))
            if msg.capitalize() != "F" and msg.capitalize() != "A" and msg.capitalize() != "S":
                print("You must type F, A, S or nothing!")
            else:
                if msg == "F":
                    currentOffers = sm.get_offers()
                    if currentOffers[pid]:
                        print("You've already done an offer. Please wait until someone accept it!")
                        break
                    cards_list = cardsXchgChoice()
                    if not cards_list:
                        break
                    sm.acquire_lock()
                    sm.set_offers(cards_list, pid)
                    currentOffers = sm.get_offers()
                    print(currentOffers)
                    sm.release_lock()
                    break
                elif msg == "A":
                    currentOffers = sm.get_offers()
                    print(currentOffers)
                    while True:
                        available = sm.get_flag()
                        print(available)
                        while True:
                            trgt = input("Please enter the number of the player you want exchange with: (or type 0 to go back) ")
                            if trgt.isnumeric():
                                trgt=int(trgt)
                                break
                            else:
                                print("What you type is not a number.")
                        if trgt == 0:
                            t = False
                            break
                        elif trgt==pid:
                            print("HAHAHA It's your own PID")
                        elif trgt not in available.keys():
                            print("No player with the ID you entered")
                        elif not (currentOffers[trgt]):
                            print("This player did not make any offer.")
                        elif available[trgt] == False:
                            print("This player is busy, either making an offer, or accepting one. Try again later.")
                        else:
                            break
                    if not verif:
                        break
                    if not (len(currentOffers[pid]) == len(currentOffers[trgt])):
                        cards_list = cardsXchgChoice()
                        if cards_list == False:
                            break
                        while not (len(cards_list) == len(currentOffers[trgt])):
                            print("You should give as many cards as there is in the offer")
                            cards_list = cardsXchgChoice()
                            if cards_list == False:
                                break
                    if cards_list == False:
                        break
                    sm.acquire_lock()
                    sm.set_offers(cards_list, pid)
                    currentOffers = sm.get_offers()
                    available = sm.get_flag()
                    available[pid] = False
                    available[trgt] = False
                    sm.release_lock()
                    # envoi d'un signal pour faire stopper la trgt
                    os.kill(trgt, signal.SIGUSR1)
                    # envoi des cards avec mq ici
                    # reception (maj des cartes en main)
                    n = 0
                    while n < len(currentOffers[pid]):
                        for k in range(len(hand)):
                            if hand[k] == cards_list[0]:
                                hand.pop(k)
                                n += 1
                                break
                    n, _ = mq.receive()
                    newCardsrcv = (n.decode()).split()
                    for l in range(len(newCardsrcv)):
                        hand.append(newCardsrcv[l])

                    offers = sm.get_offers()
                    cards = offers[pid]
                    msg = ""
                    for q in range(len(cards)):
                        msg += cards[q] + " "
                    msg = msg.encode()
                    mq.send(msg, type=3)

                    sm.acquire_lock()
                    available = sm.get_flag()
                    available[pid] = True
                    available[trgt] = True
                    currentOffers = sm.get_offers()
                    empty=[]
                    sm.set_offers(empty, pid)
                    sm.set_offers(empty, trgt)
                    sm.release_lock()
                    print(hand)
                    break
                elif msg == "S":
                    if not (len(set(hand)) == 1):
                        print("The cards are not identical")
                    else:
                        print(" __     __                               _ \n \\ \\   / /                              | |\n  \\ \\_/ /__  _   _  __      _____  _ __ | |\n   \\   / _ \\| | | | \\ \\ /\\ / / _ \\| '_ \\| |\n    | | (_) | |_| |  \\ V  V / (_) | | | |_|\n    |_|\\___/ \\__,_|   \\_/\\_/ \\___/|_| |_(_)\n                                           \n")
                        scores = sm.get_points()
                        if pid in scores.keys():
                            score = scores[pid]
                        else:
                            score = 0
                        if hand[0] == "Shoes":
                            score += 5
                        elif hand[0] == "Bike":
                            score += 4
                        elif hand[0] == "Train":
                            score += 3
                        elif hand[0] == "Car":
                            score += 2
                        elif hand[0] == "Airplane":
                            score += 1
                        sm.acquire_lock()
                        sm.set_points(score, pid)
                        sm.release_lock()
                        os.kill(ppid, signal.SIGUSR2)
                    break
