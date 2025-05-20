import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sp
import pywt
import neurokit2 as nk
from scipy.ndimage import gaussian_filter1d
from scipy.signal import medfilt

# ----------- CHARGEMENT MIS À JOUR -----------


def load_data(filepath, interval_ms=5):
    df = pd.read_csv(filepath, sep='\t', header=None,
                     encoding='ISO-8859-1', engine="python")

    df.columns = ["Time", "HR", "Av BP", "BP", "D",
                  "BP2", "Comment", "Extra"][:df.shape[1]]

    for col in ["BP", "Av BP", "HR", "D", "BP2"]:
        df[col] = pd.to_numeric(df[col].astype(
            str).str.replace(",", "."), errors="coerce")

    df.drop(columns=[c for c in ["Comment", "Extra"]
            if c in df.columns], inplace=True)
    df.dropna(inplace=True)

    df["Time"] = np.arange(0, len(df)) * (interval_ms / 1000)
    return df

# ----------- MÉTHODES DE TRAITEMENT -----------


def filter_signal(signal, sampling_rate=200):
    filters = {}

    # 1. Butterworth (0.5-45 Hz)
    try:
        nyq = 0.5 * sampling_rate
        b, a = sp.butter(2, [0.5/nyq, 45/nyq], btype='band')
        filters['butterworth'] = sp.filtfilt(b, a, signal)
    except:
        filters['butterworth'] = None

    # 2. Gaussian
    filters['gaussian'] = gaussian_filter1d(signal, sigma=2)

    # 2b. Double Gaussian (2 passes)
    try:
        double_pass = gaussian_filter1d(signal, sigma=2)
        filters['double_gaussian'] = gaussian_filter1d(double_pass, sigma=2)
    except:
        filters['double_gaussian'] = None

    # 3. Median
    filters['median'] = medfilt(signal, kernel_size=5)

    # 4. NeuroKit clean
    try:
        filters['neurokit_clean'] = nk.ecg_clean(
            signal, sampling_rate=sampling_rate, method="neurokit")
    except:
        filters['neurokit_clean'] = None

    # 5. Wavelet denoise
    try:
        coeffs = pywt.wavedec(signal, 'db4', level=4)
        threshold = np.median(
            np.abs(coeffs[-1])) / 0.6745 * np.sqrt(2 * np.log(len(signal)))
        coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]
        filters['wavelet_denoise'] = pywt.waverec(coeffs, 'db4')
    except:
        filters['wavelet_denoise'] = None

    return filters

# ----------- AFFICHAGE -----------


def plot_signals(raw_signal, filtered_dict, time, column_name="HR"):
    fig, axs = plt.subplots(len(filtered_dict) + 1, 1,
                            figsize=(14, 2.5 * (len(filtered_dict) + 1)))

    # Signal brut
    axs[0].plot(time, raw_signal, label="Signal brut", color='black')
    axs[0].set_title(f"{column_name} - Brut")
    axs[0].legend()

    # Filtres
    for i, (name, signal) in enumerate(filtered_dict.items(), start=1):
        if signal is not None:
            signal = signal[:len(time)]
            axs[i].plot(time, signal, label=name)
            axs[i].set_title(f"{column_name} - {name}")
            axs[i].legend()

    for ax in axs:
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Amplitude")

    plt.tight_layout()
    plt.show()

# ----------- MAIN -----------


if __name__ == "__main__":
    filepath = "data/data1/Sansinjection.txt"
    start_time, end_time = 15, 30
    sampling_rate = 200  # 5ms entre deux mesures
    interval_ms = 5

    df = load_data(filepath, interval_ms=interval_ms)
    min_time, max_time = df["Time"].min(), df["Time"].max()
    print(f"📌 Temps total disponible : {min_time:.2f}s à {max_time:.2f}s")

    # Fenêtrage temporel
    df = df[(df["Time"] >= start_time) & (
        df["Time"] <= end_time)].reset_index(drop=True)
    time = df["Time"].values
    raw_hr = df["HR"].values

    print("\n🔍 Traitement du signal HR")
    filtered_hr = filter_signal(raw_hr, sampling_rate=sampling_rate)

    # Affichage des signaux
    plot_signals(raw_hr, filtered_hr, time, column_name="HR")
