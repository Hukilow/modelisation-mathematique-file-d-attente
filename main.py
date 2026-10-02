import os
import socket
import sys

from streamlit.web import bootstrap


def chemin_ressource(nom_fichier):
    # Pour PYInstaller, on utilise sys._MEIPASS pour trouver le chemin du fichier
    if hasattr(sys, "_MEIPASS"):
        dossier = sys._MEIPASS
    else:
        dossier = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(dossier, nom_fichier)


def main():
    fichier_streamlit = chemin_ressource("affichage2.py")

    # On utilise un socket pour trouver un port libre
    with socket.socket() as port_socket:
        port_socket.bind(("127.0.0.1", 0))
        port = port_socket.getsockname()[1]

    # On configure les options de Streamlit pour le mode headless
    flag_options = {
        "global.developmentMode": False,
        "server.headless": True,
        "server.address": "127.0.0.1",
        "server.port": port,
        "browser.serverAddress": "127.0.0.1",
        "browser.serverPort": port,
    }
    # On charge les options de configuration et on lance l'application Streamlit
    bootstrap.load_config_options(flag_options)
    bootstrap.run(fichier_streamlit, False, [], flag_options)


if __name__ == "__main__":
    main()