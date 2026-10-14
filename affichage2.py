import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from simulation import simul_evenement_MMc_new, simul_evenement_MDc_new
import time
from fonctions_aides import mm1_theorique, mmc_theorique, md1_theorique, L_moyen_temporel, rho_temps_reel,Lq_moyen_temporel, W_moyen_temporel, Wq_moyen_temporel, moyenne_clients_par_heure, poisson_probabilite_heure, somme_poisson_probabilite, moyenne_poisson_probabilite

st.title("Les files d'attente")

# -----------------------------
# Constantes
# -----------------------------
temps_entre_update = 0.5

# -----------------------------------
# Paramètres permanents sur la gauche
# -----------------------------------
st.sidebar.title("Paramètres")

st.sidebar.header("Paramètres simulation")

# Dropdown list pour choisir le mode d'affichage
methode_affichage = st.sidebar.selectbox(
    "Type de service",
    [
        "Animation graphique",
        "Instantanément",
        "Comparaison efficacité"
    ]
)

# Input pour le nombre de client
nombre_client = st.sidebar.number_input(
    "Nombre de client",
    min_value=0,
    max_value=1000000,
    value=100,
    step=1
)



# Slider pour la vitesse de l'animation du graphique
if methode_affichage == "Animation graphique":
    vitesse_animation = st.sidebar.slider(
        "Vitesse de l'animation",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1
)
    # Slider pour le nombre de bar affichés en même temps sur l'écran
    nbr_bar = st.sidebar.slider(
        "Nombre de bar affichés",
        min_value=1,
        max_value=25,
        value=5,
        step=1
    )

# Dropdown list pour choisir seed aléatoire ou non
choix_seed = st.sidebar.selectbox(
    "Seed",
    [
        "Aléatoire",
        "Manuel"
    ]
)

if choix_seed == "Aléatoire":
    seed = np.random.randint(0, 1000000)
    st.sidebar.write(f"Seed aléatoire : {seed}")
else :
    seed = st.sidebar.number_input(
        "Seed pour la génération aléatoire",
        min_value=0,
        max_value=1000000,
        value=43747,
        step=1
    )


st.sidebar.header("Paramètres théorique")

# Slider pour le taux d'arrivée (lambda) 
lambd = st.sidebar.slider(
    "Taux d'arrivée λ (clients/heure)",
    min_value=1.0,
    max_value=30.0,
    value=18.0,
    step=1.0
)

# Slider pour le taux de service (mu)
µ = st.sidebar.slider(
    "Taux de service μ (clients/heure)",
    min_value=2.0,
    max_value=40.0,
    value=20.0,
    step=1.0
)

if methode_affichage == "Comparaison efficacité":
    µ2 = st.sidebar.slider(
        "Taux de service μ2 (clients/heure)",
        min_value=2.0,
        max_value=40.0,
        value=25.0,
        step=1.0
    )

    st.sidebar.header("Comparaison efficacité")
    # Slider pour le nombre de simulation à comparer
    nbr_simulation = st.sidebar.slider(
        "Nombre de simulation à comparer",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

st.sidebar.header("Modèle et paramètres")

# Dropdown list pour choisir le modèle
modele = st.sidebar.selectbox(
    "Type de service",
    [
        "Exponentiel — M/M/1",
        "Exponentiel — M/M/c",
        "Déterministe — M/D/1"
        ""
    ]
)

if modele == "Exponentiel — M/M/c":
    c = st.sidebar.slider(
        "Nombre de serveurs (c)",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )



# -----------------------------------
# Affichage des pamamètres et infos
# -----------------------------------


st.write(f"### Modèle choisi : {modele}")


# -----------------------------------
# Informations qui seront mises à jour
# -----------------------------
# On affiche le temps, le temps entre chaque evènement, le nombre de clients dans la file, le nombre de client servis
# p le taux d'occupation du système, L le nombre moyen de clients dans le système, W le temps moyen passé dans le système, Wq le temps moyen passé dans la file d'attente, Lq le nombre moyen de clients dans la file d'attente

col1, col2, col3, col4  = st.columns(4)


with col1:
    clientRestantCol = st.empty()

with col2:
    clientServisCol = st.empty()

with col3:
    clientDansFile = st.empty()

with col4:
    pOccupationCol = st.empty()



# pOccupationCol, WmoyenCol, WqMoyenCol, LqMoyenCol = st.columns(4)
graphique = st.empty()

# -----------------------------
# Bouton
# -----------------------------
if methode_affichage == "Animation graphique":
    temps_entre_update_reel = temps_entre_update / vitesse_animation    

if st.button("Lancer la simulation"):
    #Transformer les données pour correspondre aux paramètres de la fonction simul_evenement
    vitesse_agent = 60 / µ  # Convertir le taux de service en temps de service en secondes
    taux_evenement = 60 / lambd  # Convertir le taux d'arrivée en temps entre les événements en secondes

    match modele:
            case "Exponentiel — M/M/1":
                data = simul_evenement_MMc_new(vitesse_agent, nombre_client, taux_evenement, 1, seed)
                theorique = mm1_theorique(lambd, µ)
                c = 1
                if methode_affichage == "Comparaison efficacité":
                    dataTab = []
                    theorique2 = mm1_theorique(lambd, µ2)
                    for i in range(nbr_simulation):
                        seed_i = np.random.randint(0, 1000000)
                        data_i = simul_evenement_MMc_new(vitesse_agent, nombre_client, taux_evenement, 1, seed_i)
                        dataTab.append(data_i)
                        data_n = simul_evenement_MMc_new(60 / µ2, nombre_client, taux_evenement, 1, seed_i)
                        dataTab.append(data_n)
            case "Exponentiel — M/M/c":
                data = simul_evenement_MMc_new(vitesse_agent, nombre_client, taux_evenement, c, seed)
                theorique = mmc_theorique(lambd, µ, c)
                c = c
                if methode_affichage == "Comparaison efficacité":
                    dataTab = []
                    theorique2 = mmc_theorique(lambd, µ2, c)
                    for i in range(nbr_simulation):
                        seed_i = np.random.randint(0, 1000000)
                        data_i = simul_evenement_MMc_new(vitesse_agent, nombre_client, taux_evenement, c, seed_i)
                        dataTab.append(data_i)
                        data_n = simul_evenement_MMc_new(60 / µ2, nombre_client, taux_evenement, c, seed_i)
                        dataTab.append(data_n)
            case "Déterministe — M/D/1":
                data = simul_evenement_MDc_new(vitesse_agent, nombre_client, taux_evenement, 1, seed)
                theorique = md1_theorique(lambd, µ)
                c = 1
                if methode_affichage == "Comparaison efficacité":
                    dataTab = []
                    theorique2 = md1_theorique(lambd, µ2)
                    for i in range(nbr_simulation):
                        seed_i = np.random.randint(0, 1000000)
                        data_i = simul_evenement_MDc_new(vitesse_agent, nombre_client, taux_evenement, 1, seed_i)
                        dataTab.append(data_i)
                        data_n = simul_evenement_MDc_new(60 / µ2, nombre_client, taux_evenement, 1, seed_i)
                        dataTab.append(data_n)


    if theorique == float("inf"):
        st.write("Le système est instable (ρ ≥ 1). La file d'attente va croître indéfiniment.")
    else :

        # Affichage des valeurs théoriques

        st.write(f"### Paramètres théoriques")
        if methode_affichage == "Comparaison efficacité":
            st.write(f"## valeur théorique de µ1 = {µ}")
        col9, col10, col11 = st.columns(3)
        col12, col13, col14 = st.columns(3)
        
        col9.metric(
            "Taux d'occupation ρ",
            f"{theorique['rho'] * 100:.1f} %"
        )
        col10.metric(
            "P attente",
            f"{theorique['P_attente'] * 100:.1f} %"
        )
        col11.metric(
            "Nbr moy de clients dans système L",
            f"{theorique['L']:.2f}"
        )
        col12.metric(
            "Nbr moy de clients dans la file Lq",
            f"{theorique['Lq']:.2f}"
        )
        col13.metric(
            "Attente moyenne Wq",
            f"{theorique['Wq'] * 60:.1f} min"
        )
        col14.metric(
            "Temps moyen dans le système W",
            f"{theorique['W'] * 60:.1f} min"
        )

        if methode_affichage == "Comparaison efficacité":
            st.write(f"## valeur théorique de µ2 = {µ2}")
            col15, col16, col17 = st.columns(3)
            col18, col19, col20 = st.columns(3)

            col15.metric(
                "Taux d'occupation ρ",
                f"{theorique2['rho'] * 100:.1f} %"
            )
            col16.metric(
                "P attente",
                f"{theorique2['P_attente'] * 100:.1f} %"
            )
            col17.metric(
                "Nbr moy de clients dans système L",
                f"{theorique2['L']:.2f}"
            )
            col18.metric(
                "Nbr moy de clients dans la file Lq",
                f"{theorique2['Lq']:.2f}"
            )
            col19.metric(
                "Attente moyenne Wq",
                f"{theorique2['Wq'] * 60:.1f} min"
            )
            col20.metric(
                "Temps moyen dans le système W",
                f"{theorique2['W'] * 60:.1f} min"
            )

    # Affichage des valeurs en temps réel pendant la simulation
    client_traité = 0

    if methode_affichage == "Animation graphique":
        

        for i in range(len(data[0])):
            if data[0][i][2] == "supp":
                client_traité += 1  # Nombre de clients servis

            # Data en haut
            clientRestantCol.metric(
                "Clients restants",
                f"{nombre_client - client_traité}"
            )

            clientServisCol.metric(
                "Clients servis",
                f"{client_traité}"
            )

            clientDansFile.metric(
                "Clients dans la file",
                f"{len(data[0][i][1])}"
            )

            if modele == "Exponentiel — M/M/1" or modele == "Déterministe — M/D/1":
                valeur_rho_temps_reel = rho_temps_reel(data[0], i, 1)
            elif modele == "Exponentiel — M/M/c":
                valeur_rho_temps_reel = rho_temps_reel(data[0], i, c)

            
            pOccupationCol.metric(
                "Occupation ρ",
                f"{valeur_rho_temps_reel * 100:.1f} %"
            )

            # -----------------------------------
            # Graphique 
            # -----------------------------------
            # On prend seulement les x derniers événements
            derniers_evenements = data[0][max(0, i - nbr_bar + 1):i + 1]

            # Pour garder une échelle Y fixe pendant toute l'animation
            hauteur_max = max(
                (sum(d["temps_service"] for d in clients) for _, clients, _ in data[0]),
                default=1
            )

            rows = []

            for position_evenement, (temps, clients, type_evenement) in enumerate(derniers_evenements):

                # La position depend de l'indice, tandis que l'etiquette conserve le temps reel.
                temps_label = f"{temps:.2f}"

                if clients:
                    for position, client in enumerate(clients):
                        rows.append({
                            "evenement": position_evenement,
                            "temps": temps_label,
                            "duree": client["temps_service"],
                            "client": f"Client {position + 1}"
                        })

                else:
                    # Permet de conserver l'événement sur l'axe X
                    # même si la file est vide
                    rows.append({
                        "evenement": position_evenement,
                        "temps": temps_label,
                        "duree": 0,
                        "client": "File vide"
                    })

            df = pd.DataFrame(rows)

            fig = px.bar(
                df,
                x="evenement",
                y="duree",
                color="client",
                barmode="stack",

                labels={
                    "evenement": "Temps de simulation",
                    "duree": "Temps de service",
                    "client": "Position"
                },

                title="État de la file à chaque événement"
            )

            # Les bars sont régulièrement espacées par l'indice, mais l'axe affiche le temps reel.
            fig.update_xaxes(
                tickmode="array",
                tickvals=list(range(len(derniers_evenements))),
                ticktext=[f"{temps:.2f}" for temps, _, _ in derniers_evenements],
                dtick=1
            )

            # Évite que l'échelle verticale change
            # à chaque nouvelle barre
            fig.update_yaxes(
                range=[0, hauteur_max * 1.1]

            )

            fig.update_layout(
            bargap=0.2
            )

            graphique.plotly_chart(
                fig,
                use_container_width=True,
                key=f"graphique_{i}"
            )


            # Temps d'attente entre chaque mise à jour de l'affichage
            time.sleep(temps_entre_update_reel)

                # Affichage des valeurs de simulation 





    # Data de fin sur la simulation
    st.write(f"### Fin de simulation")
    if methode_affichage == "Comparaison efficacité":
        st.write(f"## valeur simulation (moyenne des simulations) de µ1 = {µ}")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        LclientMoyenDansSysteme = st.empty()

    with col6:
        WmoyenCol = st.empty()

    with col7:
        WqMoyenCol = st.empty()

    with col8:
        LqMoyenCol = st.empty()

    SommeProbaPoisson, MoyenneProbaPoisson, pOccupationCol = st.columns(3)

    if methode_affichage == "Comparaison efficacité":
        # On sépare les simulations en deux groupes : celles avec µ1 et celles avec µ2
        simulations_mu1 = dataTab[0::2]
        simulations_mu2 = dataTab[1::2]

        def moyennes_simulations(simulations):
            return {
                "L": np.mean([
                    L_moyen_temporel(simulation[0], len(simulation[0]) - 1)
                    for simulation in simulations
                ]),
                "Lq": np.mean([
                    Lq_moyen_temporel(simulation[0], len(simulation[0]) - 1, c)
                    for simulation in simulations
                ]),
                "W": np.mean([
                    W_moyen_temporel(simulation[1], len(simulation[1]) - 1)
                    for simulation in simulations
                ]),
                "Wq": np.mean([
                    Wq_moyen_temporel(simulation[1], len(simulation[1]) - 1)
                    for simulation in simulations
                ]),
                "SP" : np.mean([
                    somme_poisson_probabilite(simulation[0])
                    for simulation in simulations
                ]),
                "MP" : np.mean([
                    moyenne_poisson_probabilite(simulation[0])
                    for simulation in simulations
                ]),
                "RHO" : np.mean([
                    rho_temps_reel(simulation[0], len(simulation[0])-1, 1)
                    for simulation in simulations
                ])
            }

        moyennes_mu1 = moyennes_simulations(simulations_mu1)
        moyennes_mu2 = moyennes_simulations(simulations_mu2)

        LclientMoyenDansSysteme.metric(
                        "L moyen (temporel)",
                        f"{moyennes_mu1['L']:.2f}"
                    )

        LqMoyenCol.metric(
                        "Lq moyen (temporel)",
                        f"{moyennes_mu1['Lq']:.2f}"
                    )

        WmoyenCol.metric(
                        "W moyen (temporel)",
                        f"{moyennes_mu1['W']:.2f} min"
                    )

        WqMoyenCol.metric(
                        "Wq moyen (temporel)",
                        f"{moyennes_mu1['Wq']:.2f} min"
                    )

        SommeProbaPoisson.metric(
                    "Somme des probabilités de Poisson",
                    f"{moyennes_mu1['SP']:.2f}"
            )

        MoyenneProbaPoisson.metric(
                    "Probabilité moyenne par heure",
                    f"{moyennes_mu1['MP']:.2f}"
            )

        pOccupationCol.metric(
                "Occupation ρ",
                f"{moyennes_mu1['RHO'] * 100:.1f} %"
            )
    else :
        LclientMoyenDansSysteme.metric(
                        "L moyen (temporel)",
                        f"{L_moyen_temporel(data[0], len(data[0])-1):.2f}"
                    )

        LqMoyenCol.metric(
                        "Lq moyen (temporel)",
                        f"{Lq_moyen_temporel(data[0], len(data[0])-1,c):.2f}"
                    )

        WmoyenCol.metric(
                        "W moyen (temporel)",
                        f"{W_moyen_temporel(data[1], len(data[1])-1):.2f} min"
                    )

        WqMoyenCol.metric(
                        "Wq moyen (temporel)",
                        f"{Wq_moyen_temporel(data[1], len(data[1])-1):.2f} min"
                    )

        SommeProbaPoisson.metric(
                "Somme des probabilités de Poisson",
                f"{somme_poisson_probabilite(data[0]):.2f}"
        )

        MoyenneProbaPoisson.metric(
                "Probabilité moyenne par heure",
                f"{moyenne_poisson_probabilite(data[0]):.2f}"
            )

    if methode_affichage == "Instantanément":

        if modele == "Exponentiel — M/M/1" :
            valeur_rho_temps_reel = rho_temps_reel(data[0], len(data[0])-1, 1)
        elif modele == "Exponentiel — M/M/c":
            valeur_rho_temps_reel = rho_temps_reel(data[0], len(data[0])-1, c)
        elif modele == "Déterministe — M/D/1":
            valeur_rho_temps_reel = rho_temps_reel(data[0], len(data[0])-1, 1)

        
        pOccupationCol.metric(
            "Occupation ρ",
            f"{valeur_rho_temps_reel * 100:.1f} %"
        )

    if methode_affichage == "Comparaison efficacité":
        st.write(f"## valeur simulation (moyenne des simulations) de µ2 = {µ2}")

        col21, col22, col23, col24 = st.columns(4)

        with col21:
            LclientMoyenDansSysteme = st.empty()
    
        with col22:
            WmoyenCol = st.empty()
    
        with col23:
            WqMoyenCol = st.empty()
    
        with col24:
            LqMoyenCol = st.empty()
    
        SommeProbaPoisson, MoyenneProbaPoisson, pOccupationCol = st.columns(3)
        
        LclientMoyenDansSysteme.metric(
                        "L moyen (temporel)",
                        f"{moyennes_mu2['L']:.2f}"
                    )
        
    
        LqMoyenCol.metric(
                        "Lq moyen (temporel)",
                        f"{moyennes_mu2['Lq']:.2f}"
                    )
    
        WmoyenCol.metric(
                        "W moyen (temporel)",
                        f"{moyennes_mu2['W']:.2f} min"
                    )
    
        WqMoyenCol.metric(
                        "Wq moyen (temporel)",
                        f"{moyennes_mu2['Wq']:.2f} min"
                    )

        SommeProbaPoisson.metric(
                    "Somme des probabilités de Poisson",
                    f"{moyennes_mu2['SP']:.2f}"
            )

        MoyenneProbaPoisson.metric(
                    "Probabilité moyenne par heure",
                    f"{moyennes_mu2['MP']:.2f}"
                )

        pOccupationCol.metric(
                    "Occupation ρ",
                    f"{moyennes_mu2['RHO'] * 100:.1f} %"
                )

        st.write("### Gain de temps dans la file d'attente")
        gain_wq = moyennes_mu1["Wq"] - moyennes_mu2["Wq"]
        comparaison_col1, comparaison_col2, comparaison_col3 = st.columns(3)

        comparaison_col1.metric(
            "Wq moyen avec µ1",
            f"{moyennes_mu1['Wq']:.2f} min"
        )
        comparaison_col2.metric(
            "Wq moyen avec µ2",
            f"{moyennes_mu2['Wq']:.2f} min"
        )
        comparaison_col3.metric(
            "Temps gagné avec µ2",
            f"{gain_wq:.2f} min",
        )






