# Dossier `data/`

Ce dossier contient les fichiers de données brutes recueillies lors des expériences physiologiques

## Structure des fichiers `.txt`

Chaque fichier correspond à un TP et contient les colonnes suivantes (séparées par des tabulations) :

| Colonne      | Signification                             |
|--------------|-------------------------------------------|
| Time         | Temps                                     |
| BP           | Pression artérielle                       |
| Av BP        | Pression artérielle moyenne               |
| HR           | Fréquence cardiaque (Heart Rate)          |
| D            | Diurèse                                   |
| HR2          | Deuxième mesure de fréquence cardiaque    |
| Comment      | Commentaires ajoutés pendant l'expérience |
| Extra        | Colonne parfois vide ou non définie       |

 Attention :  
- Certaines lignes contiennent des valeurs invalides ou manquantes.
- La colonne "Time" peut être **non monotone** si les instruments ont été relancés.  
  → Nous utilisons donc un **temps reconstruit**, basé sur un intervalle constant de 5 ms entre les points.
- La colonne Extra n'existe pas visiuellement , mais est nécésaire pour la lecture des fichiers .txt

## Organisation interne

- `data1/` contient les fichiers du premier TP (ex: `Sansinjection.txt`, `Adrenaline.txt`, etc.).
- D’autres sous-dossiers peuvent apparaître pour des lots futurs.

## Bonnes pratiques

- Ne jamais modifier les fichiers bruts.
- Ajouter vos données personnelles dans un sous-dossier dédié (ex: `data/data3/` ; `data/data4/`; ...).
- Conservez les noms des fichiers tels qu’ils vous sont fournis.
