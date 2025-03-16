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
    df = pd.read_csv(filepath, sep='\t', names=[
                     "Time", "BP", "Av BP", "HR", "D", "HR2", "Comment"], header=0)
    time = df["Time"].values  # Colonne de temps
    signal = df["HR"].values  # Colonne contenant la fréquence cardiaque
    return time, signal

# Détection des PQRST avec Biosppy


def detect_pqrst(signal, sampling_rate=1000):
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
        "r_peaks": out[2],
        "filtered_signal": out[1],
    }

# Comparaison de différentes méthodes de détection


def test_different_methods(time, signal, methods):
    """
    Compare différentes méthodes de détection des PQRST en les appliquant sur le signal ECG.

    Args:
        time (np.ndarray): Vecteur temps du signal.
        signal (np.ndarray): Signal ECG brut.
        methods (list): Liste des méthodes à tester.

    Returns:
        dict: Résultats des différentes méthodes testées.
    """
    results = {}
    for method in methods:
        print(f"Test de la méthode : {method}")
        if method == "biosppy":
            result = detect_pqrst(signal)
        # D'autres méthodes peuvent être ajoutées ici
        else:
            result = {"r_peaks": [], "filtered_signal": signal}
        results[method] = result
    return results

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
    plt.figure(figsize=(12, 5))
    plt.plot(time, signal, label='ECG Filtré', color='b')
    plt.scatter(time[r_peaks], signal[r_peaks],
                color='r', marker='o', label='R-peaks')
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.title(f"Détection des R-peaks avec {method_name}")
    plt.legend()
    plt.show()


# Exécution du script
if __name__ == "__main__":
    filepath = "pronto.st/data/data1/Sansinjection.txt"  # Chemin du fichier
    time, signal = load_ecg_data(filepath)
    methods = ["biosppy"]  # Liste des méthodes à tester
    results = test_different_methods(time, signal, methods)

    for method, result in results.items():
        plot_ecg_with_peaks(
            time, result["filtered_signal"], result["r_peaks"], method)
