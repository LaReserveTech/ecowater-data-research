# Ecowater - Recherche Data
Ce repo est destiné à l'exploration des datas identifiées comme étant potentiellement pertinentes pour le projet Ecowater mené par La Réserve.tech

## Installation de l'environnement virtuel
### **En ayant make (et python) installé**

La commande:
```
make all
```
suffit à créer et installer l'environnement virtuel du projet. La librairie poetry sera automatiquement installée par make. Les différentes librairies du projets seront ensuite installée par poetry. Pour ajouter de nouvelles librairies à l'environnement du projet, se référer à la section `Gestion de l'environnement virtuel du projet`.

### **Avec seulement python**
1. Poetry

L'installation de ce projet se fait à l'aide de la librairie [Poetry](https://python-poetry.org/). Il est donc nécessaire d'avoir poetry préalablement installé, faisable à l'aide de `pip` :
```Bash
pip install poetry
```
2. Téléchargement des librairies/packages

```Bash
poetry install 
``` 
Cette commande installe toutes les librairies listées dans [pyproject.toml](pyproject.toml) et crée un dossier `.venv` définissant l'environnement virtuel du projet.

## Selection du kernel / de l'interpréteur python :
Afin d'exécuter un notebook depuis l'environnement virtuel, il faut s'assurer que le kernel du notebook soit l'environnement' Python du projet :

`.venv (Python 3.11.1) .venv\Scripts\python.exe`

De la même manière, il faut spécifier la version Python de l'environnement virtuel comme interpréteur Python pour VSCode. Pour ajouter de nouvelles librairies à l'environnement du projet, se référer à la section `Gestion de l'environnement virtuel du projet`.

## Gestion de l'environnement virtuel du projet
### **Activation**
```
. .venv/Scripts/activate
```
Cette commande permet d'activer l'environnement virtuel. Ainsi, toute commande dans le terminal (par exemple `python script.py` pour exécuter un script `script.py`) s'exécutera au sein de l'environnement virtuel défini par le projet (et bénéficiera donc des librairies installées pour le projet).

### **Désactivation**
```
deactivate
```
Cette commande permet de quitter l'environnement virtuel si ce dernier est activé.

### **Ajout d'une librairie à l'environnement virtuel**
Après avoir activé l'environnement virtuel :
```
poetry add <librairie>
```
Cette commande va ajouter la librairie au pyproject.toml et la télécharger dans l'environnement virtuel du projet. `poetry add <librairie>` remplace donc entièrement `pip install <librairie>`.
Pour installer numpy, il suffira donc d'exécuter :
```
poetry add numpy
```
### **Commandes supplémentaires**
De nombreuses autres commandes existent et peuvent être utiles pour un projet, telles que :
- `poetry update` : met à jour les librairies
- `poetry remove <librairie>` : supprime une librairie 
- `poetry self update` : met poetry à jour
- `poetry lock` : vérifie les versions des libraires sans les installer

Toutes les commandes disponibles sont listées [ici](https://python-poetry.org/docs/cli/).

### **Note** 
L'interêt de Poetry par rapport à pip est sa gestion des versions des dépendances des différentes librairies, plus d'informations là-dessus [ici](https://python-poetry.org/docs/master/managing-dependencies/).
