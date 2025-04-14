# 💡 PRONTO.ST — Physiological signal decomposition and generation

Bienvenue dans le projet **PRONTO.ST** (Décomposition et génération de série temporelle pour la physiologie) !  
Ce projet vise à analyser, nettoyer et visualiser des signaux physiologiques (ECG, pression artérielle, diurèse, etc.) obtenus lors d’expériences de laboratoire.

---

## 📁 Organisation du projet

```
pronto.st/
│
├── data/                  # Données brutes du projet
│   └── data1/             # Dossier contenant les fichiers .txt physiologiques
│
├── notebooks/             # Fichiers Jupyter pour exploration, traitement, visualisation
│   ├── exemple_format.ipynb    # Exemple de chargement + visualisation
│
├── scr/                   # Fichiers Python réutilisables
│   ├── traitement_signal.py    # Traitement des signaux par diverses méthodes
│   ├── main.py                 # Fichier principal (à créer en fin de projet)
│
├── results/               # Résultats finaux, graphiques, exports éventuels
│
├── README.md              # Vous êtes ici
├── requirements.txt       # Liste des dépendances Python à installer
└── .gitignore             # Fichiers/dossiers à exclure du suivi Git (à définir)
```

---

## 🚀 Installation

1. **Cloner ce dépôt :**

```bash
git clone https://github.com/VKND02/pronto.st.git
cd pronto.st
```

2. **Créer un environnement Python (optionnel mais recommandé) :**

```bash
python -m venv venv
source venv/bin/activate  # ou 'venv\Scripts\activate' sous Windows
```

3. **Installer les dépendances :**

```bash
pip install -r requirements.txt
```

---

## 📊 Objectifs

- Lire et afficher des signaux physiologiques bruts
- Débruiter les signaux avec différentes bibliothèques (NeuroKit2, Scipy, etc.)
- Comparer plusieurs méthodes de filtrage
- Extraire les ondes PQRST, les fréquences cardiaques, etc.
- Préparer des visualisations claires pour l’analyse
- Generer de nouvelle données

---

## 💼 Fichiers utiles

- `exemple_format.ipynb` : démonstration d’un chargement de fichier + affichage
- `traitement_signal.py` : fonctions de nettoyage du signal
- `README.md` dans `/data/` : infos sur l’organisation des fichiers .txt
- `main.py` : à venir en fin de projet

---

## 👨‍👩‍👧‍👦 Pour les contributeurs

Merci de suivre les conventions suivantes :

- Respecter l’organisation des dossiers
- Nommer clairement vos fichiers (`exploration_nom.ipynb`, `analyse_X.py`, etc.)
- Ajouter une description courte en haut de chaque script
- Ne pas modifier directement `main.py` sans concertation

Un fichier `fiche_convention.md` sera fourni pour les bonnes pratiques à suivre 📑

---

## 📬 Contact

Créateur principal : [VKND02](https://github.com/VKND02)  
Projet réalisé dans le cadre de l'UE Pronto
