import sysv_ipc
import threading
import random
from collections import Counter

key = 300
keyjeu = 400
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
mqjeu = sysv_ipc.MessageQueue(keyjeu, sysv_ipc.IPC_CREAT)
playing = True
bell_lock = threading.Lock()
offres_lock = threading.Lock()


def deck():
    deck = []
    transports = ["Shoes", "Bike", "Train", "Car", "Airplane"]
    for j in transports[:n]:
        for _ in range(5):
            deck.append(j)
    random.shuffle(deck)
    return deck


def bell(pid):
    bell_lock.acquire()
    list = mains[pid]
    if list.count(list[0]) == len(list):
        for i in continuer:
            continuer[i] = False
            win = "L'utilisateur" + str(pid) + " a gagné."
            mq.send(win.encode(), type=i)
    bell_lock.release()


# sera invoque chaque fois que quelqu'un update le dictionnaire offres
#def offer_display():
    mes = str(offres).encode()
    for pid in players:
        mqjeu.send(mes, type=int(str(pid) + 1))


def make_offer(pid, list):
    offres_lock.acquire()
    offres[pid] = list
    offres_lock.release()
    #offer_display()
    pass


def accept_offer():
    offres_lock.acquire()
    offres_lock.release()
    #offer_display()
    pass

# To see if the offer that has been made is indeed in the hand of the player
def valide(list, pid):
    c1, c2 = Counter(list), Counter(mains[pid])
    for k, n in c1.items():
        if n > c2[k]:
            return False
    return True



def jouer(pid):
    mes = "Ton identifiant est: " + str(pid) + '\n' + "Votre main est: " + str(mains[pid])
    mes = mes.encode()
    mqjeu.send(mes, type=pid)
    while playing:
        if not continuer[pid]:
            break
        mes = "Que voulez vous faire? Faire une offre(F), en accepter une(A) ou faire sonner la sonnerie(S) ?"
        mes = mes.encode()
        mqjeu.send(mes, type=pid)
        # The answer of the choice
        while True:
            m, _ = mqjeu.receive(type=pid)
            m = m.decode()
            if m == "F":
                if offres[pid]:
                    msg = "Vous ne pouvez pas faire plus d'une offre"
                    msg = msg.encode()
                    mqjeu.send(msg, type=pid)
                    break
                else:
                    msg = "Quelles cartes voulez-vous proposer ? (Par exemple: Shoes Shoes)"
                    msg = msg.encode()
                    mqjeu.send(msg, type=pid)
                    while True:
                        echange, t = mqjeu.receive(type=pid)
                        echange = (echange.decode()).split()
                        if echange != "":
                            if valide(echange, pid):
                                make_offer(pid, echange)
                                effectue = "Votre offre a été effectué avec succès. Votre nouvelle main est " + str([x for x in mains[pid] if x not in echange])
                                effectue = effectue.encode()
                                mqjeu.send(effectue, type=pid)
                                break
                            else:
                                msg = "Vous n'avez pas les cartes que vous pretendez avoir"
                                msg = msg.encode()
                                mqjeu.send(msg, type=pid)
                                break
                    break
            # elif m =="A":

            else:
                bell(pid)

#premier thread ne se lance pas?
def connection():
    cartes = deck()
    k = 0
    t = True
    threads = []
    while True:
        pid, _ = mq.receive(type=1)
        pid = int(pid.decode())
        if len(players) < n:
            players.append(pid)
            offres[pid] = []
            mains[pid] = cartes[k:k + 5]
            scores[pid] = 0
            dispo[pid] = True
            continuer[pid] = True
            mes = "Tu es accepté dans la partie. En attente d'autres joueurs..."
            mq.send(mes, type=pid)
            play = threading.Thread(target=jouer, args=(pid,))
            threads.append(play)
            print("Il manque {} joueurs".format(n - len(players)))
        if t and len(players) == n:
            print("La partie commence")
            for i in threads:
                i.start()
            t = False
        if len(players) >= n:
            mes = "La partie est pleine"
            mes = mes.encode()
            mq.send(mes, type=pid)
        k += 5


if __name__ == "__main__":
    #Techniquement c'est une shared memory vu qu'on est sur le meme process et les threads utilisent la meme memoire
    players = []
    offres = {}
    mains = {}
    scores = {}
    dispo = {}
    continuer = {}
    n = int(input("Combien de joueurs dans la partie : "))
    connection = threading.Thread(target=connection)
    connection.start()
    connection.join()
