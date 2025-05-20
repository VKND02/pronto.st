import neurokit2 as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_ecg_data(filepath, start_time, end_time):
    """Charge les données ECG et filtre entre start_time et end_time."""
    try:
        df = pd.read_csv(filepath, sep='\t', header=None,
                         encoding='ISO-8859-1', engine='python')
        df.columns = ["Time", "HR", "Av BP", "BP", "D",
                      "BP2", "Comment", "Extra"][:df.shape[1]]
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
    filepath = "data/data1/Sansinjection.txt"  # Chemin du fichier ECG
    start_time, end_time = 300, 310  # Plage temporelle
    sampling_rate = 100  # Modifier si nécessaire

    df = load_ecg_data(filepath, start_time, end_time)

    if df is not None:
        ecg_signal = df["HR"].values
        time = df["Time"].values

        # === Définition des filtres à tester ===
        filter_methods = {
            "Butterworth (0.5-45Hz)": nk.signal_filter(ecg_signal, sampling_rate=sampling_rate, lowcut=0.5, highcut=45, method="butterworth"),
            "Butterworth (legacy)": nk.signal_filter(ecg_signal, sampling_rate=sampling_rate, lowcut=0.5, highcut=45, method="butterworth_ba"),
            "FIR (0.5-45Hz)": nk.signal_filter(ecg_signal, sampling_rate=sampling_rate, lowcut=0.5, highcut=45, method="fir"),
            "Bessel (0.5-45Hz)": nk.signal_filter(ecg_signal, sampling_rate=sampling_rate, lowcut=0.5, highcut=45, method="bessel"),
            "Savitzky-Golay": nk.signal_filter(ecg_signal, sampling_rate=sampling_rate, lowcut=0.5, highcut=45, method="savgol", order=2),
            "Powerline (50Hz)": nk.signal_filter(ecg_signal, sampling_rate=sampling_rate, method="powerline", powerline=50)
        }

        # === Affichage des résultats ===
        num_plots = len(filter_methods) + 1  # +1 pour le signal brut
        fig, axes = plt.subplots(num_plots, 1, figsize=(12, 2 * num_plots))

        # Affichage du signal brut
        axes[0].plot(time, ecg_signal,
                     label="ECG Brut (sans filtrage)", color='black', alpha=0.8)
        axes[0].set_xlabel("Temps (s)")
        axes[0].set_ylabel("Amplitude")
        axes[0].set_title("ECG Brut (sans filtrage)")
        axes[0].legend()

        # Affichage des signaux filtrés
        for ax, (filter_name, signal) in zip(axes[1:], filter_methods.items()):
            ax.plot(time, signal, label=filter_name, alpha=0.7)
            ax.set_xlabel("Temps (s)")
            ax.set_ylabel("Amplitude")
            ax.set_title(filter_name)
            ax.legend()

        plt.tight_layout()
        plt.show()
