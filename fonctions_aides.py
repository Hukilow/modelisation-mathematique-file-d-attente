import math
import numpy as np

# Fonctions théoriques 
# -------------------

# Fonction théorique MM1
# ---------------------
# Prend en entrée le taux d'arrivée (lambda) et le taux de service (mu)
# Retourne un dictionnaire avec les valeurs théoriques de rho, L, W, Wq et Lq
# rho = taux d'occupation du système
# P_attente = probabilité qu'un client attende dans la file
# L = nombre moyen de clients dans le système
# W = temps moyen passé dans le système
# Wq = temps moyen passé dans la file d'attente
# Lq = nombre moyen de clients dans la file d'attente
# --------------------
def mm1_theorique(lambd, µ):
    p = lambd / µ

    if p >= 1:
        return float("inf")

    L = p / (1 - p)
    W = 1 / (µ - lambd)
    Wq = W - 1 / µ
    Lq = lambd * Wq
    P_attente = p # en MM1 : attende = serveur occupé donc P_attente = p

    return {"rho": p, "L": L, "W": W, "Wq": Wq, "Lq": Lq, "P_attente": P_attente}


# Fonction théorique MMC
# ---------------------
# Prend en entrée le taux d'arrivée (lambda), le taux de service (mu) et le nombre de serveurs (c)
# Retourne un dictionnaire avec les valeurs théoriques de rho, P_attente, L, W, Wq et Lq
# rho = taux d'occupation du système
# P_attente = probabilité qu'un client attende dans la file
# L = nombre moyen de clients dans le système
# W = temps moyen passé dans le système
# Wq = temps moyen passé dans la file d'attente
# Lq = nombre moyen de clients dans la file d'attente
# ---------------------
def mmc_theorique(lambd, µ, c):
    a = lambd / µ
    p = lambd / (c * µ)

    if p >= 1:
        return float("inf")

    somme = sum((a ** n) / math.factorial(n) for n in range(c))
    dernier = (a ** c) / (math.factorial(c) * (1 - p))

    P0 = 1 / (somme + dernier)
    P_attente = dernier * P0
    Wq = P_attente / (c * µ - lambd)
    W = Wq + 1 / µ
    Lq = lambd * Wq
    L = lambd * W

    return {"rho": p, "P_attente" : P_attente, "L": L, "W": W, "Wq": Wq, "Lq": Lq}

# Fonction théorique M/D/1
# ---------------------
# Prend en entrée le taux d'arrivée (lambda) et le taux de service (mu)
# Retourne un dictionnaire avec les valeurs théoriques de rho, P_attente, L, W, Wq et Lq
# rho = taux d'occupation du système
# P_attente = probabilité qu'un client attende dans la file
# L = nombre moyen de clients dans le système
# W = temps moyen passé dans le système
# Wq = temps moyen passé dans la file d'attente
# Lq = nombre moyen de clients dans la file d'attente
# ---------------------
def md1_theorique(lambd, µ):
    p = lambd / µ

    if p >= 1:
        return float("inf")

    Wq = p / (2 * µ * (1 - p))
    W = Wq + 1 / µ
    Lq = lambd * Wq
    L = lambd * W
    P_attente = p # en M/D/1 : attende = serveur occupé donc P_attente = p

    return {"rho": p, "P_attente" : P_attente, "L": L, "W": W, "Wq": Wq, "Lq": Lq}


# Fonctions de simulation 
# -------------------

# Fonction pour calculer le taux d'occupation du système jusqu'à un certain événement
# ---------------------
# Prend en entrée les données de la simulation, l'indice de l'événement et le nombre de serveurs
# Retourne le taux d'occupation du système jusqu'à l'événement
# ---------------------
def rho_temps_reel(data, i, c=1):
    temps_occupe = 0.0
    duree_totale = 0.0
    for k in range(i):
        dt = data[k + 1][0] - data[k][0]
        nb_serveurs_occupes = min(c, len(data[k][1]))  # en M/M/c
        fraction_occupation = nb_serveurs_occupes / c  # entre 0 et 1
        temps_occupe += fraction_occupation * dt
        duree_totale += dt
    return temps_occupe / duree_totale if duree_totale > 0 else 0


# Fonction pour calculer la moyenne temporelle du nombre de clients dans le système jusqu'à un certain événement
# ---------------------
# Prend en entrée les données de la simulation et l'indice de l'événement
# Retourne la moyenne temporelle du nombre de clients dans le système jusqu'à l'événement
# --------------------- 
def L_moyen_temporel(data, i):

    # roh = rho_temps_reel(data, i)
    # return roh / (1 - roh) if roh < 1 else float("inf")
    if i == 0:
        return len(data[0][1])
    somme_ponderee = 0.0
    duree_totale = 0.0
    for k in range(i):
        dt = data[k + 1][0] - data[k][0]
        Lk = len(data[k][1])
        somme_ponderee += Lk * dt
        duree_totale += dt
    return somme_ponderee / duree_totale if duree_totale > 0 else 0

#Fonction pour calculer la moyenne temporelle du nombre de clients dans la file jusqu'à un certain événement
# ---------------------
# Prend en entrée les données de la simulation et l'indice de l'événement
# Retourne la moyenne temporelle du nombre de clients dans la file jusqu'à l'événement
# ---------------------
def Lq_moyen_temporel(data, i, c=1):
    if i == 0:
        return len(data[0][1])
    somme_ponderee = 0.0
    duree_totale = 0.0
    for k in range(i):
        dt = data[k + 1][0] - data[k][0]
        Lk = len(data[k][1])-c  # On soustrait c pour ne pas compter le(s) client(s) en service 
        if Lk < 0:
            Lk = 0
        somme_ponderee += Lk * dt
        duree_totale += dt
    return somme_ponderee / duree_totale if duree_totale > 0 else 0



#Fonction pour calculer le temps moyen passé dans le système jusqu'à un certain événement
# ---------------------
# Prend en entrée les données de la simulation et l'indice de l'événement
# Retourne le temps moyen passé dans le système jusqu'à l'événement
# ---------------------


def W_moyen_temporel(data, i):
    somme = 0
    for j in range(i):
        somme += data[j]["temps_global"]
    return somme/i



# #Fonction pour calculer le temps moyen passé dans la file jusqu'à un certain événement
# # ---------------------
# # Prend en entrée les données de la simulation et l'indice de l'événement
# # Retourne le temps moyen passé dans la file jusqu'à l'événement
# # ---------------------
def Wq_moyen_temporel(data, p):

    somme = 0
    for i in range(p):
        somme += data[i]["temps_global"]-data[i]["temps_initial"]
    return somme/p



# #Fonction pour calculer le nombre moyen de clients arrivant dans la file par heures
# # ---------------------
# # Prend en entrée les données de la simulation
# # Retourne le nombre moyen de clients arrivant dans la file par heures pour toutes la durée de la simulation
# # ---------------------
def moyenne_clients_par_heure(data):
    if len(data) < 2:
        return 0
    duree_totale = data[-1][0] - data[0][0]
    nombre_clients = sum(1 for event in data if event[2] == "add")
    return (nombre_clients / duree_totale) * 60 if duree_totale > 0 else 0

# #Fonction pour calculer la probalité d'un nombre de clients arrivant dans la file selon une heure précise
# # ---------------------
# # Prend en entrée les données de la simulation et l'heure précise
# # Retourne la probabilité que le nombre de clients arrivant dans la file selon cette heure précise soit arrivé
# # ---------------------
def poisson_probabilite_heure(data, heure):
    if len(data) < 2:
        return 0
    moy_clients_par_heure = moyenne_clients_par_heure(data)
    # Calcul du nombre de clients arrivant dans la file selon l'heure précise
    k = sum(
        1
    for event in data
    if event[2] == "add" and event[0] // 60 == heure)
    # Calcul de la proba selon la loi de Poisson
    probabilite = (math.exp(-moy_clients_par_heure) * ((moy_clients_par_heure ** k)) / math.factorial(k))
    return probabilite

# vérif si la fonction est bonne là

# #Fonction pour calculer la somme des probabilités d'un nombre de clients arrivant dans la file selon une heure précise
# # ---------------------
# # Prend en entrée les données de la simulation
# # Retourne la somme des probabilités que le nombre de clients arrivant dans la file selon une heure précise soit arrivé
# # ---------------------

def somme_poisson_probabilite(data):
    if len(data) < 2:
        return 0
    somme_probabilite = 0
    for heure in range(24):
        somme_probabilite += poisson_probabilite_heure(data, heure)
    return somme_probabilite

