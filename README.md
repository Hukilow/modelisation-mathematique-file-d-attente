

# Comment compiler (créer le .exe)
## Créer le .venv
`py -m venv .venv`

## Se mettre dans le .venv
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
`.\.venv\Scripts\Activate.ps1`

## Installer les dépendances 
`python -m pip install -r requirements.txt`

## Créer le .exe depuis Simulation.spec
`.\.venv\Scripts\pyinstaller.exe --noconfirm --clean --distpath . .\Simulation.spec`

## Déplacer les fichiers du dossier Simulation dans le dossier root et supprimer le dossier Simulation
`Get-ChildItem .\Simulation -Force | Move-Item -Destination . -Force`
`Remove-Item .\Simulation -Recurse -Force`

# Lancer le projet
`.\Simulation.exe`

# Lancer le projet directement avec Python

## Créer le .venv
`py -m venv .venv`

## Activer le .venv
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
`\.\.venv\Scripts\Activate.ps1`

## Installer les dépendances
`python -m pip install -r requirements.txt`

## Lancer l'application
`python main.py`

L'application affiche l'adresse locale dans le terminal. Ouvrir cette adresse
dans un navigateur, puis utiliser `Ctrl+C` dans le terminal pour arrêter
l'application.

## Désactiver le .venv
`deactivate`
