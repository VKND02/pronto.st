import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from biosppy.signals import ecg

# Chargement des données ECG depuis le fichier "Sansinjection.txt"


def load_ecg_data(filepath):
    """
    Charge les données ECG depuis un fichier texte et extrait le signal de fréquence cardiaque (HR).

    Args:
        filepath (str): Chemin du fichier contenant les données ECG.

    Returns:
        np.ndarray: Signal HR extrait.
        np.ndarray: Temps associé aux échantillons.
    """
    try:
        df = pd.read_csv(filepath, sep='\t', names=[
                         "Time", "BP", "Av BP", "HR", "D", "HR2", "Comment"], header=0, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        print("⚠️ Erreur d'encodage. Tentative avec UTF-8...")
        df = pd.read_csv(filepath, sep='\t', names=[
                         "Time", "BP", "Av BP", "HR", "D", "HR2", "Comment"], header=0, encoding='utf-8', errors='replace')

    # Conversion des colonnes en numérique
    df["Time"] = pd.to_numeric(df["Time"], errors='coerce')
    df["HR"] = pd.to_numeric(df["HR"], errors='coerce')

    # Suppression des lignes contenant des NaN
    df.dropna(inplace=True)

    time = df["Time"].values  # Colonne de temps
    signal = df["HR"].values  # Colonne contenant la fréquence cardiaque

    # Vérifier la taille du signal
    if len(signal) < 1000:  # Minimum 1000 échantillons requis pour BioSPPy
        raise ValueError(
            "Le signal ECG est trop court pour être analysé. Vérifiez les données.")

    return time, signal

# Détection des PQRST avec Biosppy


def detect_pqrst(signal, sampling_rate=200):
    """
    Applique Biosppy pour détecter les ondes PQRST sur un signal ECG.

    Args:
        signal (np.ndarray): Signal ECG brut.
        sampling_rate (int): Fréquence d'échantillonnage en Hz.

    Returns:
        dict: Contient les indices des R-peaks et le signal filtré.
    """
    out = ecg.ecg(signal=signal, sampling_rate=sampling_rate, show=False)
    return {
        "r_peaks": out["rpeaks"],
        "filtered_signal": out["filtered"],
    }

# Tracé du signal avec les pics détectés


def plot_ecg_with_peaks(time, signal, r_peaks, method_name):
    """
    Affiche le signal ECG et marque les R-peaks détectés pour une méthode donnée.

    Args:
        time (np.ndarray): Vecteur temps du signal.
        signal (np.ndarray): Signal ECG filtré.
        r_peaks (np.ndarray): Indices des R-peaks détectés.
        method_name (str): Nom de la méthode utilisée.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(time, signal, label='ECG Filtré', color='black')
    plt.scatter(time[r_peaks], signal[r_peaks],
                color='r', marker='o', label='R-peaks')
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.title(f"Détection des R-peaks avec {method_name}")
    plt.legend()
    plt.show()


# Exécution du script
if __name__ == "__main__":
    filepath = "data/data1/Sansinjection.txt"  # Chemin du fichier
    try:
        time, signal = load_ecg_data(filepath)

        # Détection des R-peaks avec BioSPPy
        result = detect_pqrst(signal)

        # Affichage des résultats
        plot_ecg_with_peaks(
            time, result["filtered_signal"], result["r_peaks"], "BioSPPy")
    except ValueError as e:
        print(f"❌ Erreur: {e}")
