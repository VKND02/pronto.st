# PRONTO.ST — Décomposition et génération de série temporelle pour l'apprentissage de la physiologie

**PRONTO.ST** est un projet développé à l’IMT Atlantique (Nantes, 2025) dans le cadre de l’UE PRONTO.  
Il vise à lire, analyser et générer des signaux physiologiques cardiaques (HR, ECG, BP), via un pipeline modulaire entièrement codé en Python.

---

## Objectif général

Le pipeline complet suit ces étapes :

1. Chargement de fichiers physiologiques bruts
2. Détection des R-peaks
3. Analyse de l’amplitude (enveloppe du signal)
4. Extraction d’une tendance lente
5. Génération d’un signal synthétique calé sur les vraies données
6. Ajout d’un bruit contrôlé
7. Visualisation (plots statiques + animation en option)

Tout est orchestré dans `main.ipynb`.

---

## Organisation du projet

```
pronto.st/
├── data/                  # Données brutes (.txt), encodées ISO-8859-1, séparées par tabulations
│   └── data1/             # Données expérimentales (TP1)
├── notebooks/             # Fichiers Jupyter (.ipynb) d’orchestration
├── scr/                   # Scripts Python modulaires (un fichier par classe)
├── results/               # Résultats ou figures exportées
├── README.md              # Ce fichier
├── requirements.txt       # Dépendances Python
└── conventions_pronto.md  # Conventions de nommage et structuration
```

---

## ▶️ Exécution rapide

1. Cloner le dépôt :

```bash
git clone https://github.com/VKND02/pronto.st.git
cd pronto.st
```

2. (Optionnel) Créer un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # ou 'venv\Scripts\activate' sous Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Lancer `main.ipynb` dans VSCode ou JupyterLab pour exécuter le pipeline pas à pas.

---

## Objectifs pédagogiques

- Apprendre à manipuler des signaux physiologiques
- Structurer un projet Python modulaire
- Mettre en œuvre des méthodes d’analyse de signal
- Créer des signaux synthétiques réalistes
- Développer un pipeline réutilisable, commenté et documenté

## Pour les contributeurs

Merci de suivre les conventions suivantes :

- Respecter l’organisation des dossiers
- Nommer clairement vos fichiers (`exploration_nom.ipynb`, `analyse_X.py`, etc.)
- Ajouter une description courte en haut de chaque script

Un fichier `fiche_convention.md` sera fourni pour les bonnes pratiques à suivre

---

## Contact

Créateur principal : [VKND02](https://github.com/VKND02)  
Projet réalisé dans le cadre de l'UE Pronto