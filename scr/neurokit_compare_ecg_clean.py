import neurokit2 as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_ecg_data(filepath, start_time, end_time):
    """
    Charge les données ECG depuis un fichier texte tabulé et extrait uniquement les colonnes Time et HR.
    Ne garde que les données comprises entre start_time et end_time.
    """
    try:
        df = pd.read_csv(filepath, sep='\t', header=None,
                         encoding='ISO-8859-1', engine='python')
        df.columns = ["Time", "BP", "Av BP", "HR", "D",
                      "HR2", "Comment", "Extra"][:df.shape[1]]
        df = df[["Time", "HR"]]

        # Conversion des valeurs en nombres (remplacement des virgules)
        df["Time"] = df["Time"].astype(str).str.replace(
            ',', '.', regex=True).astype(float)
        df["HR"] = df["HR"].astype(str).str.replace(
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
        ecg_signal = df["HR"].values
        # Utiliser la colonne "Time" pour l'axe des temps
        time = df["Time"].values
        sampling_rate = 100  # Modifier si besoin

        # Vérifier si le signal ECG contient suffisamment de données
        if len(ecg_signal) < sampling_rate * 2:
            print("❌ Trop peu de données pour l'analyse ECG.")
        else:
            # Liste des méthodes de nettoyage disponibles
            methods = ["neurokit", "biosppy", "pantompkins1985", "hamilton2002",
                       "elgendi2010", "engzeemod2012", "vg"]

            # Exclure "engzeemod2012" si fs < 96 Hz
            if sampling_rate <= 96:
                methods.remove("engzeemod2012")

            # Dictionnaire pour stocker les signaux nettoyés
            cleaned_signals = {}

            # Appliquer toutes les méthodes de nettoyage
            for method in methods:
                try:
                    cleaned_signals[method] = nk.ecg_clean(
                        ecg_signal, sampling_rate=sampling_rate, method=method)
                except Exception as e:
                    print(f"⚠️ Erreur avec la méthode {method}: {e}")
                    cleaned_signals[method] = None

            # === Affichage des signaux ===
            num_methods = len(cleaned_signals) + 1  # +1 pour le signal brut
            fig, axes = plt.subplots(
                num_methods, 1, figsize=(12, 2 * num_methods))

            # Affichage du signal brut
            axes[0].plot(
                time, ecg_signal, label="ECG Brut (sans filtrage)", color='black', alpha=0.8)
            axes[0].set_xlabel("Temps (s)")
            axes[0].set_ylabel("Amplitude")
            axes[0].set_title("ECG Brut (sans filtrage)")
            axes[0].legend()

            # Affichage des signaux nettoyés
            for ax, (method, signal) in zip(axes[1:], cleaned_signals.items()):
                if signal is not None:
                    ax.plot(time, signal,
                            label=f"ECG Cleaned ({method})", alpha=0.7)
                    ax.set_xlabel("Temps (s)")
                    ax.set_ylabel("Amplitude")
                    ax.set_title(f"ECG Nettoyé - {method}")
                    ax.legend()

            plt.tight_layout()
            plt.show()
