import os
import sys
from streamlit.web import cli as stcli


def chemin_ressource(nom_fichier):
    # Lorsque le programme est compilé avec PyInstaller
    if hasattr(sys, "_MEIPASS"):
        dossier = sys._MEIPASS
    else:
        dossier = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(dossier, nom_fichier)


def main():
    fichier_streamlit = chemin_ressource("affichage2.py")

    sys.argv = [
        "streamlit",
        "run",
        fichier_streamlit,
        "--server.address=localhost",
    ]

    sys.exit(stcli.main())


if __name__ == "__main__":
    main()