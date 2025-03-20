import neurokit2 as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_ecg_data(filepath, start_time, end_time):
    """
    Charge les données ECG depuis un fichier texte tabulé et extrait uniquement les colonnes Time, HR et HR2.
    Ne garde que les données comprises entre start_time et end_time.
    """
    try:
        df = pd.read_csv(filepath, sep='\t', header=None,
                         encoding='ISO-8859-1', engine='python')
        df.columns = ["Time", "BP", "Av BP", "HR", "D",
                      "HR2", "Comment", "Extra"][:df.shape[1]]
        df = df[["Time", "HR", "HR2"]]

        # Conversion des valeurs en nombres (remplacement des virgules)
        df["Time"] = df["Time"].astype(str).str.replace(
            ',', '.', regex=True).astype(float)
        df["HR"] = df["HR"].astype(str).str.replace(
            ',', '.', regex=True).astype(float)
        df["HR2"] = df["HR2"].astype(str).str.replace(
            ',', '.', regex=True).astype(float)

        # Supprimer les valeurs manquantes
        df.dropna(inplace=True)

        # Déterminer le temps minimum et maximum disponible
        min_time, max_time = df["Time"].min(), df["Time"].max()
        print(f"📌 Temps minimum : {min_time}s | Temps maximum : {max_time}s")

        # Vérifier et ajuster les bornes demandées
        start_time = max(start_time, min_time)
        end_time = min(end_time, max_time)

        # Filtrer les données entre start_time et end_time
        df = df[(df["Time"] >= start_time) & (df["Time"] <= end_time)]

        print(f"✅ Données ECG chargées entre {start_time}s et {end_time}s !")
        return df
    except Exception as e:
        print(f"❌ Erreur lors du chargement du fichier : {e}")
        return None


if __name__ == "__main__":
    filepath = "data/data1/Sansinjection.txt"

    # Définir la plage de temps souhaitée
    start_time = 13.9  # Début à ... secondes
    end_time = 50  # Fin à ... secondes

    df = load_ecg_data(filepath, start_time, end_time)

    if df is not None:
        ecg_signal_hr = df["HR"].values
        ecg_signal_hr2 = df["HR2"].values
        time = df["Time"].values
        sampling_rate = 100  # Modifier si besoin

        # Vérifier si le signal ECG contient suffisamment de données
        if len(ecg_signal_hr) < sampling_rate * 2:
            print("❌ Trop peu de données pour l'analyse ECG.")
        else:
            # Affichage du signal HR et HR2
            plt.figure(figsize=(12, 6))
            plt.plot(time, ecg_signal_hr,
                     label="HR (Fréquence cardiaque principale)", color='blue', alpha=0.8)
            plt.plot(time, ecg_signal_hr2,
                     label="HR2 (Deuxième mesure FC)", color='red', alpha=0.7)
            plt.xlabel("Temps (s)")
            plt.ylabel("Amplitude")
            plt.title("Comparaison HR vs HR2")
            plt.legend()
            plt.show()
