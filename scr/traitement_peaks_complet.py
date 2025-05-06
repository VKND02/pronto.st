import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sp
import pywt
import neurokit2 as nk
import biosppy.signals.ecg as biosppy_ecg
from scipy.ndimage import gaussian_filter1d
from scipy.signal import medfilt


def load_data(filepath, interval_ms=5):
    df = pd.read_csv(filepath, sep='\t', header=None, encoding='ISO-8859-1', engine="python")
    df.columns = ["Time", "HR", "Av BP", "BP", "D", "BP2", "Comment", "Extra"][:df.shape[1]]

    for col in ["BP", "Av BP", "HR", "D", "BP2"]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")

    df.drop(columns=[c for c in ["Comment", "Extra"] if c in df.columns], inplace=True)
    df.dropna(inplace=True)
    df["Time"] = np.arange(0, len(df)) * (interval_ms / 1000)
    return df


def filter_signal(signal, sampling_rate=200):
    filters = {}

    nyq = 0.5 * sampling_rate
    try:
        b, a = sp.butter(2, [0.5/nyq, 45/nyq], btype='band')
        filters['butterworth'] = sp.filtfilt(b, a, signal)
    except:
        filters['butterworth'] = None

    filters['gaussian'] = gaussian_filter1d(signal, sigma=2)
    filters['gaussian2x'] = gaussian_filter1d(filters['gaussian'], sigma=2)
    filters['median'] = medfilt(signal, kernel_size=5)

    try:
        filters['neurokit_clean'] = nk.ecg_clean(signal, sampling_rate=sampling_rate, method="neurokit")
    except:
        filters['neurokit_clean'] = None

    try:
        coeffs = pywt.wavedec(signal, 'db4', level=4)
        threshold = np.median(np.abs(coeffs[-1])) / 0.6745 * np.sqrt(2 * np.log(len(signal)))
        coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]
        filters['wavelet_denoise'] = pywt.waverec(coeffs, 'db4')
    except:
        filters['wavelet_denoise'] = None

    return filters


def detect_peaks_biosppy(signal, sampling_rate):
    out = biosppy_ecg.ecg(signal=signal, sampling_rate=sampling_rate, show=False)
    return out["rpeaks"]


def detect_peaks_neurokit(signal, sampling_rate):
    try:
        processed = nk.ecg_process(signal, sampling_rate=sampling_rate)
        return processed[1]["ECG_R_Peaks"].values
    except:
        return []


def plot_peaks(time, raw_signal, filters, peaks_dict, title_suffix):
    fig, axs = plt.subplots(len(filters) + 1, 1, figsize=(14, 3 * (len(filters) + 1)))
    axs[0].plot(time, raw_signal, label="Signal brut", color="black")
    axs[0].set_title("HR - Signal brut")
    axs[0].legend()

    for i, (name, signal) in enumerate(filters.items(), start=1):
        if signal is not None:
            signal = signal[:len(time)]
            axs[i].plot(time, signal, label=name)
            if name in peaks_dict:
                axs[i].scatter(time[peaks_dict[name]], signal[peaks_dict[name]], color='red', s=30, label="R-peaks")
            axs[i].set_title(f"HR - {name} ({title_suffix})")
            axs[i].legend()

    for ax in axs:
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Amplitude")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    filepath = "data/data1/Sansinjection.txt"
    start_time, end_time = 13.9, 30
    sampling_rate = 200
    interval_ms = 5

    df = load_data(filepath, interval_ms=interval_ms)
    df = df[(df["Time"] >= start_time) & (df["Time"] <= end_time)].reset_index(drop=True)
    time = df["Time"].values
    raw_hr = df["HR"].values

    filtered = filter_signal(raw_hr, sampling_rate=sampling_rate)

    biosppy_peaks = {}
    for method, sig in filtered.items():
        if sig is not None:
            biosppy_peaks[method] = detect_peaks_biosppy(sig[:len(time)], sampling_rate)

    plot_peaks(time, raw_hr, filtered, biosppy_peaks, title_suffix="BioSPPy")

    neurokit_peaks = {}
    for method, sig in filtered.items():
        if sig is not None:
            neurokit_peaks[method] = detect_peaks_neurokit(sig[:len(time)], sampling_rate)

    plot_peaks(time, raw_hr, filtered, neurokit_peaks, title_suffix="NeuroKit2")
