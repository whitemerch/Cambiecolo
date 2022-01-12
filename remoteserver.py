from multiprocessing.managers import BaseManager
from multiprocessing import Lock

class MyRemoteClass:

    def __init__(self):
        self.available= {}
        self.offer= {}
        self.lock= Lock()

    def get_flag(self):
        return self.available

    def set_flag(self, pushed_bool, key):
        self.available[key]=pushed_bool

    def get_offers(self):
        return self.offers

    def set_offers(self, pushed_list, key):
        self.offers[key] = pushed_list


class MyManager(BaseManager):
    pass

n = int(input("Combien de joueurs dans la partie : "))
remote = MyRemoteClass(n)

MyManager.register('sm', callable=lambda:remote)
m = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
s = m.get_server()
s.serve_forever()


#_______________________________________________________________________________#
#code a copier dans client
from multiprocessing.managers import BaseManager

class MyManager(BaseManager): pass
MyManager.register('sm')
m = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
m.connect()
#_______________________________________________________________________________#

#_______________________________________________________________________________#
#_______________________________________________________________________________#
#_______________________________________________________________________________#
#bloc while true pour les offres avec remote server (dans client)

signal.signal(signal.SIGUSR2, handler)
signal.signal(signal.SIGUSR3, handler2)

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
                    sm.set_offers(current)
                    print(current)
                    sm.release_lock()
                elif msg == "A":
                    current = sm.get_offers()
                    print(current)
                    while true:
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


def handler(sig, frame):
    if sig==signal.SIGUSR1:
        mq.receive...
        #maj main
        mq.Send...

def handler2(sig, frame):
    if sig==signal.SIGUSR3
        print("quelqu'un à remporté cette manche")
        sys.exit(1)



def valide (list, pid):
    c1, c2 = Counter(list), Counter(mains[pid])
    for k, n in c1.items():
        if n>c2[k]:
            return False


#_______________________________________________________________________________#
#_______________________________________________________________________________#
#_______________________________________________________________________________#
