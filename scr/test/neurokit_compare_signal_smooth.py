import neurokit2 as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_ecg_data(filepath, start_time, end_time):
    """Charge les données ECG et filtre entre start_time et end_time."""
    try:
        df = pd.read_csv(filepath, sep='\t', header=None,
                         encoding='ISO-8859-1', engine='python')
        df.columns = ["Time", "BP", "Av BP", "HR", "D",
                      "HR2", "Comment", "Extra"][:df.shape[1]]
        df = df[["Time", "HR"]]

        df["Time"] = df["Time"].astype(str).str.replace(
            ',', '.', regex=True).astype(float)
        df["HR"] = df["HR"].astype(str).str.replace(
            ',', '.', regex=True).astype(float)
        df.dropna(inplace=True)

        min_time, max_time = df["Time"].min(), df["Time"].max()
        print(f"📌 Temps minimum : {min_time}s | Temps maximum : {max_time}s")

        start_time = max(start_time, min_time)
        end_time = min(end_time, max_time)

        df = df[(df["Time"] >= start_time) & (df["Time"] <= end_time)]
        print(f"✅ Données ECG chargées entre {start_time}s et {end_time}s !")
        return df
    except Exception as e:
        print(f"❌ Erreur lors du chargement du fichier : {e}")
        return None


if __name__ == "__main__":
    filepath = "data/data1/Ocytocine.txt"
    start_time, end_time = 300, 310
    sampling_rate = 100  # Modifier si nécessaire

    df = load_ecg_data(filepath, start_time, end_time)

    if df is not None:
        ecg_signal = df["HR"].values
        time = df["Time"].values

        # 📌 Liste des méthodes de lissage
        smoothing_methods = {
            "Moving Average": nk.signal_smooth(ecg_signal, method="moving_average", window_size=5),
            "Gaussian": nk.signal_smooth(ecg_signal, method="gaussian", window_size=5),
            "Convolution": nk.signal_smooth(ecg_signal, method="convolution", window_size=5),
            "Savitzky-Golay": nk.signal_smooth(ecg_signal, method="savgol", window_size=5, polyorder=2),
        }

        # === Affichage des résultats ===
        num_plots = len(smoothing_methods) + 1  # +1 pour le signal brut
        fig, axes = plt.subplots(num_plots, 1, figsize=(12, 2 * num_plots))

        # Affichage du signal brut
        axes[0].plot(time, ecg_signal,
                     label="ECG Brut (sans filtrage)", color='black', alpha=0.8)
        axes[0].set_xlabel("Temps (s)")
        axes[0].set_ylabel("Amplitude")
        axes[0].set_title("ECG Brut (sans filtrage)")
        axes[0].legend()

        # Affichage des signaux lissés
        for ax, (method, signal) in zip(axes[1:], smoothing_methods.items()):
            ax.plot(time, signal, label=f"ECG Lissé - {method}", alpha=0.7)
            ax.set_xlabel("Temps (s)")
            ax.set_ylabel("Amplitude")
            ax.set_title(f"ECG Lissé - {method}")
            ax.legend()

        plt.tight_layout()
        plt.show()
