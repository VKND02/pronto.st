import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sp
import pywt
import neurokit2 as nk
import biosppy.signals.ecg as biosppy_ecg
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


# ----------- FILTRAGE MULTI-MÉTHODES -----------

def filter_signal(signal, sampling_rate=200):
    filters = {}

    # 1. Filtrage Butterworth (0.5-45 Hz)
    try:
        nyq = 0.5 * sampling_rate
        b, a = sp.butter(2, [0.5/nyq, 45/nyq], btype='band')
        filters['butterworth'] = sp.filtfilt(b, a, signal)
    except:
        filters['butterworth'] = None

    # 2. Gaussian Filter
    filters['gaussian'] = gaussian_filter1d(signal, sigma=2)

    # 3. Median Filter
    filters['median'] = medfilt(signal, kernel_size=5)

    # 4. NeuroKit2 Clean ECG
    try:
        filters['neurokit_clean'] = nk.ecg_clean(
            signal, sampling_rate=sampling_rate, method="neurokit")
    except:
        filters['neurokit_clean'] = None

    # 5. Wavelet Denoising
    try:
        coeffs = pywt.wavedec(signal, 'db4', level=4)
        threshold = np.median(
            np.abs(coeffs[-1])) / 0.6745 * np.sqrt(2 * np.log(len(signal)))
        coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]
        filters['wavelet_denoise'] = pywt.waverec(coeffs, 'db4')
    except:
        filters['wavelet_denoise'] = None

    return filters


# ----------- DÉTECTION PQRST via BioSPPy -----------

def detect_peaks_biosppy(signal, sampling_rate):
    output = biosppy_ecg.ecg(
        signal=signal, sampling_rate=sampling_rate, show=False)
    r_peaks = output["rpeaks"]
    filtered_signal = output["filtered"]

    q_peaks, s_peaks, p_peaks, t_peaks = [], [], [], []
    q_window, s_window, p_window = int(
        0.05 * sampling_rate), int(0.05 * sampling_rate), int(0.15 * sampling_rate)

    for i, r in enumerate(r_peaks):
        start_q, end_q = max(r - q_window, 0), r
        q_peaks.append(np.argmin(filtered_signal[start_q:end_q]) + start_q)

        start_s, end_s = r, min(r + s_window, len(filtered_signal))
        s_peaks.append(np.argmin(filtered_signal[start_s:end_s]) + start_s)

        start_p, end_p = max(q_peaks[-1] - p_window, 0), q_peaks[-1]
        p_peaks.append(np.argmax(filtered_signal[start_p:end_p]) + start_p)

        if i < len(r_peaks) - 1:
            next_r = r_peaks[i+1]
        else:
            next_r = len(filtered_signal)
        t_offset, margin = int(0.02 * sampling_rate), int(0.05 * sampling_rate)
        start_t = s_peaks[-1] + t_offset if s_peaks else 0
        end_t = max(next_r - margin, start_t + 1)
        t_peaks.append(np.argmax(filtered_signal[start_t:end_t]) + start_t)

    return filtered_signal, r_peaks, q_peaks, s_peaks, p_peaks, t_peaks


# ----------- AFFICHAGE DES SIGNAUX -----------

def plot_signals_with_peaks(time, raw, filtered, r, q, s, p, t):
    plt.figure(figsize=(15, 5))
    plt.plot(time, raw, label="Brut", color="lightgray")
    plt.plot(time, filtered[:len(time)],
             label="Filtré (BioSPPy)", color="black")
    plt.scatter(time[r], filtered[r], color="red", label="R-peaks")
    plt.scatter(time[q], filtered[q], color="green", label="Q-peaks")
    plt.scatter(time[s], filtered[s], color="magenta", label="S-peaks")
    plt.scatter(time[p], filtered[p], color="cyan", label="P-peaks")
    plt.scatter(time[t], filtered[t], color="yellow", label="T-peaks")

    plt.title("Détection des ondes PQRST")
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ----------- MAIN -----------

if __name__ == "__main__":
    filepath = "data/data1/Ocytocine.txt"
    start_time = 0
    end_time = 20
    interval_ms = 5
    sampling_rate = int(1000 / interval_ms)

    df = load_data(filepath, interval_ms=interval_ms)
    time = df["Time"].values
    hr_signal = df["HR"].values

    print(f"📌 Temps total disponible : {time.min():.2f}s à {time.max():.2f}s")
    print("🔍 Traitement de HR et détection des pics...")

    filters = filter_signal(hr_signal, sampling_rate=sampling_rate)

    if filters["butterworth"] is not None:
        filtered_signal, r, q, s, p, t = detect_peaks_biosppy(
            filters["butterworth"], sampling_rate)
        plot_signals_with_peaks(
            time, hr_signal, filtered_signal, r, q, s, p, t)
    else:
        print("⚠️ Aucun signal filtré disponible pour la détection des pics.")
