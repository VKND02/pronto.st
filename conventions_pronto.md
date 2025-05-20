## Conventions de Rédaction des Fichiers (`.py` / `.ipynb`) – Projet PRONTO.ST

Ce document précise les **bonnes pratiques** à suivre pour structurer proprement le code Python et les notebooks du projet PRONTO.ST.

---

### Organisation recommandée du dépôt

```
pronto.st/
├── data/                  # Données brutes (.txt encodées ISO-8859-1, séparées par tabulations)
│   ├── data1/             # Fichiers issus du TP1
│   └── README.md          # Explication du format des données
│
├── notebooks/             # Notebooks Jupyter (orchestration du pipeline ou tests)
│   ├── main.ipynb         # Notebook principal
│   └── README.md
│
├── scr/                   # Scripts Python modulaires (un fichier par classe)
│   ├── data_loader.py
│   ├── peak_detector.py
│   ├── amplitude_analyzer.py
│   ├── trend_extractor.py
│   ├── signal_generator.py
│   ├── noise_injector.py
│   └── README.md
│
├── results/               # Résultats (images, figures exportées, vidéos)
├── requirements.txt       # Dépendances Python
├── README.md              # Présentation globale du projet
└── conventions_pronto.md  # Ce document
```

---

### Fichiers Python `.py`

#### À faire :

- Organiser le code autour d’une **classe unique par fichier** (`.py`)
- Nommer le fichier comme la classe (ex. `amplitude_analyzer.py`)
- Documenter la classe et ses méthodes avec des **docstrings claires**
- Utiliser des **chemins relatifs** (`../data/data1/`)
- Respecter l’ordre suivant :
  1. Imports (`numpy`, `matplotlib`, etc.)
  2. Classe avec ses méthodes
  3. Eventuel bloc `if __name__ == "__main__":` (facultatif ici)

#### Exemple minimal :

```python
import numpy as np
import matplotlib.pyplot as plt

class Exemple:
    """Classe de démonstration"""
    def __init__(self, x):
        self.x = x

    def calculer(self):
        return self.x ** 2
```

#### À éviter :
- Mélanger plusieurs classes dans un même fichier
- Placer du code hors fonction ou classe
- Copier/coller du code non documenté

---

### Fichiers Jupyter `.ipynb`

#### À faire :
- Commencer par un **titre** et une **brève description** du notebook
- Ajouter des **commentaires avant chaque cellule** de code :
  - Que fait-on ? Pourquoi cette étape ?
- Nettoyer avant commit :
  - Supprimer les cellules inutiles
  - Éviter les sorties trop longues ou inutiles

#### À éviter :
- Code sans explication
- Notebooks désorganisés ou expérimentaux non rangés

---

### Bonnes pratiques générales

- **Versionner uniquement les notebooks utiles** (pas les tests jetables)
- **Commenter chaque graphique**
- Ajouter des titres, légendes, labels aux figures `matplotlib`

---

— Victor (PRONTO.ST)
