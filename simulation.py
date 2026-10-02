from statistics import mean

import numpy as np

# E[T] = 1 / Lambda
# E[T] * Lambda = 1
#Lambda = 1 / E[T]

#E[T]
duree_moyenne_minute = 18/60

#Lambda
taux= 1 / duree_moyenne_minute

def simul_naif(vitesse_agent,temps_max_simul,taux_evenement):
    file = []
    attente = 1
    for i in range (temps_max_simul):
        attente = attente - 1 #passer le temps

        if file !=[]: #Si il y a un client
            file[0] = file[0] - 1#passer le temps
            if file[0] == 0: #Si le client a fini
                file.remove(file[0])
                print("retire : ",file)

        if attente == 0: #Nouveau client
            file.append(vitesse_agent)
            print("ajout : ",file)
            attente = round(np.random.exponential(taux_evenement),1) * 60


def simul_evenement(vitesse_agent,temps_max_simul,taux_evenement):
    result = []
    file = []
    temps_gobal = 0 #duree de la simulation
    while temps_gobal < temps_max_simul:
        attente = round(np.random.exponential(taux_evenement), 1) * 60
        temps_gobal += attente

        if file != []:  # Si il y a un client
            while attente > 0:
                if file == []:
                    attente = -1
                else:
                    temp = file[0]
                    file[0] = file[0] - attente
                    if file[0] <= 0:
                        file.remove(file[0])
                    attente = attente - temp

        file.append(vitesse_agent)
        result.append((temps_gobal,file.copy()))
        print("ajout : ", file)
    return result

def agent_travaille(beau_graph,file,c,i,temps_agent,restant,result):
    while restant > 0:
        if len(file) > i:
            temp = file[i]
            file[i] = file[i] - restant  # il passe le temps avec le client
            if file[i] < 0:  # si le client est servie
                i += c  # on passe au suivant (1 client ne peut etre servie que par un agent)
                beau_graph.remove(temp)
                temps_agent += temp
                result.append((round(temps_agent, 2), beau_graph.copy(), "supp"))

            restant = round(restant - temp, 2)  # si l'agent a encore le temps, il fait un autre client
        else:
            restant = 0  # si il y a plus de client , il ne fait rie,

def simul_evenement_MMc_file_unique(taux_vitesse_agent,client_max_simul,taux_evenement,c=1,s=2):
    rng = np.random.default_rng(seed=s)
    file = []
    result = []
    temps_gobal = 0 #duree de la simulation
    nb_client = 0
    while nb_client < client_max_simul or file != []:
        nb_client += 1
        if nb_client > client_max_simul:
            attente = sum(file) +0.01
        else:
            attente = rng.exponential(taux_evenement)#Temps avant qu'un autre client arrive EN MINUTE


        beau_graph = file.copy()
        for i in range (c): #Pour chaque agent
            agent_travaille(beau_graph,file,c,i,temps_gobal,attente,result)
        for x in file.copy():  # on retire tous les client qui on fini
            if x < 0:
                file.remove(x)

        temps_gobal += attente  # Temps general

        if not nb_client > client_max_simul:
            file.append(rng.exponential(taux_vitesse_agent)) #le nouveau client avec son temps EN MINUTE
            result.append((temps_gobal, file.copy(),"add"))
    return result

def simul_evenement_MDc_file_unique(taux_vitesse_agent,client_max_simul,taux_evenement,c=1,s=2):
    rng = np.random.default_rng(seed=s)
    file = []
    result = []
    temps_gobal = 0 #duree de la simulation
    nb_client = 0
    while nb_client < client_max_simul or file != []:
        nb_client += 1
        if nb_client > client_max_simul:
            attente = sum(file) +0.01
        else:
            attente = rng.exponential(taux_evenement)#Temps avant qu'un autre client arrive EN MINUTE


        beau_graph = file.copy()
        for i in range (c): #Pour chaque agent
            agent_travaille(beau_graph,file,c,i,temps_gobal,attente,result)

        for x in file.copy(): #on retire tous les client qui on fini
            if x < 0:
                file.remove(x)
        temps_gobal += attente  # Temps general

        if not nb_client > client_max_simul:
            ## LA SEUL LIGNE QUI CHANGE
            file.append(taux_vitesse_agent) #le nouveau client avec son temps EN MINUTE
            result.append((temps_gobal, file.copy(),"add"))
    return result

def simul_evenement_MMc_file_priorite(taux_vitesse_agent,client_max_simul,taux_evenement,c=1,s=2):
    rng = np.random.default_rng(seed=s)
    file = []
    result = []
    temps_gobal = 0 #duree de la simulation
    nb_client = 0
    while nb_client < client_max_simul or file != []:
        nb_client += 1
        if nb_client > client_max_simul:
            attente = sum(file) +0.01
        else:
            attente = rng.exponential(taux_evenement)#Temps avant qu'un autre client arrive EN MINUTE

        file.sort() ## LA SEUL LIGNE QUI CHANGE
        beau_graph = file.copy()
        for i in range (c): #Pour chaque agent
            agent_travaille(beau_graph,file,c,i,temps_gobal,attente,result)

        for x in file.copy(): #on retire tous les client qui on fini
            if x < 0:
                file.remove(x)
        temps_gobal += attente  # Temps general

        if not nb_client > client_max_simul:
            file.append(rng.exponential(taux_vitesse_agent)) #le nouveau client avec son temps EN MINUTE
            result.append((temps_gobal, file.copy(),"add"))
    return result

def nombre_client_moyen(simul,nb_client): #L
    somme = 0
    for i in simul:
        if (i[2] == "add"):
            somme += len(i[1])
    return somme/nb_client

# print(simul_evenement(60*3,60*60,taux))
# data = simul_evenement(60*3,60*60,taux)
# # data = simul_evenement_MMc_file_unique(60/20,15,60/18,2,0)

# print("dqdqzd")
# print(data)


# nbr = 0
# for i in range(len(data)):
#     if data[i][2] == "supp":
#         nbr += 1
# print("Nombre de supp : ",nbr)



##Nouveau
def simul_evenement_MMc_new(taux_vitesse_agent,client_max_simul,taux_evenement,c=1,s=2):
    rng = np.random.default_rng(seed=s)
    file = []
    result = []
    liste_clients = []
    temps_gobal = 0 #duree de la simulation
    nb_client = 0
    while nb_client < client_max_simul or file != []:
        nb_client += 1
        if nb_client > client_max_simul:
            attente = 99999999999
        else:
            attente = rng.exponential(taux_evenement)#Temps avant qu'un autre client arrive EN MINUTE

        while attente > 0 and not nb_client == 0:
                    if file == []:
                        # Le serveur est libre et on attend un nouveau client pendant `attente`.
                        # On doit avancer temps_gobal de cette durée, sinon les moments où la
                        # file est vide sont invisibles dans result et rho_temps_reel / L_moyen_temporel
                        # sous-estiment la fraction de temps avec file vide.
                        temps_gobal = temps_gobal + attente
                        attente = -1
                    else:
                        t = min (len(file),c)
                        minus = 999999999
                        for i in file[0:t]:
                            minus = min(minus,i["temps_service"])

                        first_client_fini = min(minus,attente)

                        for i in range(len(file[0:t])):
                            file[i]["temps_service"] = file[i]["temps_service"] - first_client_fini

                        for i in range(len(file)):
                            file[i]["temps_global"] += first_client_fini

                        attente = attente - first_client_fini
                        temps_gobal = temps_gobal + first_client_fini

                        for i in file.copy():
                            if i["temps_service"] == 0:
                                # Le client vient de finir son service : on le retire de la file
                                # AVANT de prendre le snapshot, sinon le client "zéro" est compté
                                # comme encore présent pendant tout l'intervalle suivant.
                                file.remove(i)
                                liste_clients.append(i)
                                # Deep copy des dicts pour que chaque snapshot dans result
                                # ait ses propres valeurs (sinon les mutations ultérieures
                                # sur les dicts écrasent les valeurs des events précédents)
                                snapshot = [dict(client) for client in file]
                                result.append((temps_gobal, snapshot, "supp"))

        if not nb_client > client_max_simul:
            client = {"temps_service":rng.exponential(taux_vitesse_agent),"temps_global":0}
            client["temps_initial"] = client["temps_service"]
            file.append(client) #le nouveau client avec son temps EN MINUTE
            snapshot = [dict(d) for d in file]
            result.append((temps_gobal, snapshot, "add"))

    return (result,liste_clients)

def simul_evenement_MDc_new(taux_vitesse_agent,client_max_simul,taux_evenement,c=1,s=2):
    rng = np.random.default_rng(seed=s)
    file = []
    result = []
    liste_clients = []
    temps_gobal = 0 #duree de la simulation
    nb_client = 0
    while nb_client < client_max_simul or file != []:
        nb_client += 1
        if nb_client > client_max_simul:
            attente = 99999999999
        else:
            attente = rng.exponential(taux_evenement)#Temps avant qu'un autre client arrive EN MINUTE

        while attente > 0 and not nb_client == 0:
                    if file == []:
                        # Le serveur est libre et on attend un nouveau client pendant `attente`.
                        # On doit avancer temps_gobal de cette durée, sinon les moments où la
                        # file est vide sont invisibles dans result et rho_temps_reel / L_moyen_temporel
                        # sous-estiment la fraction de temps avec file vide.
                        temps_gobal = temps_gobal + attente
                        attente = -1
                    else:
                        t = min (len(file),c)
                        minus = 999999999
                        for i in file[0:t]:
                            minus = min(minus,i["temps_service"])

                        first_client_fini = min(minus,attente)

                        for i in range(len(file[0:t])):
                            file[i]["temps_service"] = file[i]["temps_service"] - first_client_fini

                        for i in range(len(file)):
                            file[i]["temps_global"] += first_client_fini

                        attente = attente - first_client_fini
                        temps_gobal = temps_gobal + first_client_fini

                        for i in file.copy():
                            if i["temps_service"] == 0:
                                # Le client vient de finir son service : on le retire de la file
                                # AVANT de prendre le snapshot, sinon le client "zéro" est compté
                                # comme encore présent pendant tout l'intervalle suivant.
                                file.remove(i)
                                liste_clients.append(i)
                                # Deep copy des dicts pour que chaque snapshot dans result
                                # ait ses propres valeurs (sinon les mutations ultérieures
                                # sur les dicts écrasent les valeurs des events précédents)
                                snapshot = [dict(client) for client in file]
                                result.append((temps_gobal, snapshot, "supp"))

        if not nb_client > client_max_simul:
            client = {"temps_service":taux_vitesse_agent,"temps_global":0}
            client["temps_initial"] = client["temps_service"]
            file.append(client) #le nouveau client avec son temps EN MINUTE
            snapshot = [dict(d) for d in file]
            result.append((temps_gobal, snapshot, "add"))

    return (result,liste_clients)

