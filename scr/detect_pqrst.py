import pandas as pd
import numpy as np
import biosppy.signals.ecg as ecg
import matplotlib.pyplot as plt

# Chargement des données ECG depuis "Sansinjection.txt"


def load_ecg_data(filepath):
    """
    Charge les données ECG depuis un fichier texte tabulé et extrait le signal HR.

    Args:
        filepath (str): Chemin du fichier contenant les données ECG.

    Returns:
        np.ndarray: Signal ECG extrait.
        np.ndarray: Temps associé aux échantillons.
    """
    df = pd.read_csv(filepath, sep='\t', names=[
                     "Time", "BP", "Av BP", "HR", "D", "HR2", "Comment"], header=0, encoding='ISO-8859-1')
    # Conversion en numérique
    df["HR"] = pd.to_numeric(df["HR"], errors='coerce')
    df["Time"] = pd.to_numeric(df["Time"], errors='coerce')
    df.dropna(inplace=True)  # Suppression des valeurs NaN

    time = df["Time"].values
    signal = df["HR"].values

    return time, signal

# Détection des PQRST avec BioSPPy


def detect_pqrst(signal, sampling_rate=200):
    """
    Détecte les ondes PQRST sur un signal ECG à l'aide de BioSPPy.

    Args:
        signal (np.ndarray): Signal ECG brut.
        sampling_rate (int): Fréquence d'échantillonnage en Hz.

    Returns:
        dict: Contient les indices des pics détectés et le signal filtré.
    """
    if len(signal) < 1000:
        raise ValueError(
            f"Le signal est trop court ({len(signal)} échantillons). Il doit avoir au moins 1000 points.")

    out = ecg.ecg(signal=signal, sampling_rate=sampling_rate, show=False)
    return {
        "filtered_signal": out["filtered"],
        "r_peaks": out["rpeaks"]
    }

# Tracé du signal avec les pics détectés


def plot_ecg_with_peaks(time, signal, r_peaks):
    """
    Affiche le signal ECG avec les pics détectés.

    Args:
        time (np.ndarray): Vecteur temps du signal.
        signal (np.ndarray): Signal ECG filtré.
        r_peaks (np.ndarray): Indices des R-peaks détectés.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(time, signal, label='ECG Filtré', color='black')
    plt.scatter(time[r_peaks], signal[r_peaks],
                color='r', marker='o', label='R-peaks')
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.title("Détection des R-peaks avec BioSPPy")
    plt.legend()
    plt.show()


# Exécution du script
if __name__ == "__main__":
    filepath = "data/data1/Sansinjection.txt"  # Chemin du fichier
    try:
        time, signal = load_ecg_data(filepath)
        result = detect_pqrst(signal)
        plot_ecg_with_peaks(time, result["filtered_signal"], result["r_peaks"])
    except ValueError as e:
        print(f"❌ Erreur: {e}")
