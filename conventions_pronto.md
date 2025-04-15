## 🧾 Conventions de Rédaction des Fichiers (`.py` / `.ipynb`) – Projet PRONTO

Voici un petit guide des **bonnes pratiques** à adopter pour rédiger vos scripts Python et notebooks Jupyter.

---

### 📁 Organisation recommandée du dossier `pronto.st`

```
pronto.st/
│
├── data/                  # Données brutes ou prétraitées (non versionnées)
│   ├── README_data.md          # Présentation de l'organisation des fichiers .txt
│   └── data1/             # Données du TP1, c'est à dire tout les fichiers .txt en rapport avec le TP1.
│
├── notebooks/             # Tous les fichiers Jupyter (.ipynb)
│   └── traitement_exemple.ipynb
│
├── scr/                   # Scripts Python (.py)
│   ├── exemple_format.py
│   └── traitement_signal.py
│
├── results/               # Graphiques et résultats exportés (optionnel)
│
├── README.md              # Présentation générale du projet
├── requirements.txt       # Liste des bibliothèques nécessaires
└── conventions_pronto.md  # Ce fichier
```

---

### 🐍 Fichiers Python `.py`

#### ✅ À faire :

- Mettre un bloc `if __name__ == "__main__":` à la fin.
- Organiser votre code avec **des fonctions claires** (pas tout dans le main).
- Documenter chaque fonction avec une **docstring** :
```python
def charger_donnees(...):
    """
    Charge un fichier texte PRONTO et retourne un DataFrame nettoyé.
    Paramètres :
        ...
    Retourne :
        pd.DataFrame
    """
```

- Utiliser des **chemins relatifs** : `../data/data1/...`
- Inclure des blocs d'import clairs, tout en haut :
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

- Respecter l’ordre logique suivant :
  1. Imports
  2. Fonctions
  3. Bloc principal `main`

#### 🚫 À éviter :
- Écrire du code en-dehors de fonctions, sauf dans le `main`.
- Copier-coller du code brut sans explication ou commentaire.

Voir exemple_format.py dans ma branch Victor

---

### 📓 Fichiers Jupyter `.ipynb`

#### ✅ À faire :
- **Commenter vos cellules** (avant ou après le code) pour expliquer :
  - Ce que vous testez
  - Ce que vous observez
- Garder un notebook propre et lisible :
  - Supprimez les cellules inutiles
  - Évitez les longues sorties non pertinentes

- Donner un **titre clair** en première cellule :  
  _"Exploration des données - Injection Adrénaline"_  
  Et une description rapide du but du notebook.

- Si besoin, utilisez `df.head()`, `df.info()` etc. pour donner du contexte aux données.

#### 🚫 À éviter :
- Des cellules sans aucun commentaire.
- Du code copié sans adaptation.
- Des notebooks trop longs sans structure.

---


Voir chargement_data.ipynb dans ma branch Victor

### 🧪 Exemple de bonne structure (dans un script)

```python
# Imports
import pandas as pd
import matplotlib.pyplot as plt

# Fonctions
def charger_donnees(filepath):
    """Charge un fichier et nettoie les colonnes"""
    ...

def afficher_signaux(df):
    """Affiche un graphique pour chaque colonne physiologique"""
    ...

# Main
if __name__ == "__main__":
    df = charger_donnees("../data/data1/Adrenaline.txt")
    afficher_signaux(df)
```

---


— Victor
