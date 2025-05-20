import pandas as pd


def load_ecg_data(filepath):
    """
    Charge les données ECG depuis un fichier texte tabulé et extrait uniquement les colonnes nécessaires.

    Args:
        filepath (str): Chemin du fichier contenant les données ECG.

    Returns:
        pd.DataFrame: Données formatées avec les colonnes numériques utiles.
    """
    try:
        # Charger le fichier avec tabulation comme séparateur
        df = pd.read_csv(filepath, sep='\t', header=None,
                         encoding='ISO-8859-1', engine='python')

        # Assigner les noms de colonnes utiles
        df.columns = ["Time", "BP", "Av BP", "HR", "D",
                      "HR2", "Comment", "Extra"][:df.shape[1]]

        # Suppression des colonnes inutiles (Comment et Extra)
        df = df[["Time", "BP", "Av BP", "HR", "D", "HR2"]]

        # Conversion des valeurs numériques
        numeric_cols = ["Time", "BP", "Av BP", "HR", "D", "HR2"]
        for col in numeric_cols:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Suppression des valeurs NaN
        df.dropna(inplace=True)

        print("✅ Fichier chargé et colonnes utiles extraites avec succès !")
        print("🔍 Aperçu des 10 premières lignes:")
        print(df.head(10))

        return df
    except Exception as e:
        print(f"❌ Erreur lors du chargement du fichier : {e}")
        return None


# Exécution du script
if __name__ == "__main__":
    filepath = "data/data1/Sansinjection.txt"  # Chemin du fichier
    df = load_ecg_data(filepath)
    if df is not None:
        print("📏 Nombre de lignes dans le fichier après nettoyage :", len(df))
