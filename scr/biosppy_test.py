import biosppy.signals.ecg as biosppy_ecg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt


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


def butter_bandpass_filter(signal, lowcut, highcut, fs, order=4):
    """
    Applique un filtre passe-bande Butterworth sur le signal.
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)


def moving_average(signal, window_size=5):
    """
    Applique un lissage par moyenne mobile.
    """
    return np.convolve(signal, np.ones(window_size)/window_size, mode='same')


if __name__ == "__main__":
    filepath = "data/data1/Sansinjection.txt"

    # Définir la plage de temps souhaitée
    start_time = 10  # Début à ... secondes
    end_time = 30  # Fin à ... secondes

    df = load_ecg_data(filepath, start_time, end_time)

    if df is not None:
        ecg_signal = df["HR"].values
        time = df["Time"].values
        sampling_rate = 100  # Modifier si besoin

        # Vérifier si le signal ECG est inversé et le corriger si nécessaire
        if np.median(ecg_signal) < 0:
            print("⚠️ Signal inversé détecté. Correction appliquée.")
            ecg_signal = -ecg_signal

        # === 1. PRÉ-FILTRAGE avec SciPy (Butterworth) ===
        ecg_filtered = butter_bandpass_filter(
            ecg_signal, lowcut=0.5, highcut=40, fs=sampling_rate)

        # === 2. LISSEMENT du signal (Moyenne Mobile) ===
        ecg_smoothed = moving_average(ecg_filtered, window_size=5)

        # Vérifier si le signal contient assez de points
        if len(ecg_smoothed) < sampling_rate * 2:
            print("❌ Trop peu de données pour l'analyse ECG.")
        else:
            # Détection des ondes PQRST avec BioSPPy
            out = biosppy_ecg.ecg(signal=ecg_smoothed,
                                  sampling_rate=sampling_rate, show=False)
            filtered_signal = out["filtered"]
            r_peaks = out["rpeaks"]

            # Tracé du signal ECG avec les R-peaks détectés
            plt.figure(figsize=(12, 6))
            plt.plot(time, filtered_signal,
                     label="ECG Filtré (BioSPPy)", color='black')
            plt.scatter(time[r_peaks], filtered_signal[r_peaks],
                        color='red', label="R-peaks")

            plt.xlabel("Temps (s)")
            plt.ylabel("Amplitude")
            plt.title(
                f"Détection des ondes ECG avec BioSPPy ({start_time}s - {end_time}s)")
            plt.legend()
            plt.show()

            # Affichage des indices détectés
            print("Detected R-peaks indices:", r_peaks)
