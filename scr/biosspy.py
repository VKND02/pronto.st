import biosppy.signals.ecg as biosppy_ecg
import numpy as np
import pandas as pd
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
    start_time = 0  # Début à ... secondes
    end_time = 10  # Fin à ... secondes

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
            # Détection des ondes PQRST avec BioSPPy
            out = biosppy_ecg.ecg(
                signal=ecg_signal, sampling_rate=sampling_rate, show=False)
            filtered_signal = out["filtered"]
            r_peaks = out["rpeaks"]

            # Détection des autres pics avec des heuristiques
            q_peaks, s_peaks, p_peaks, t_peaks = [], [], [], []
            q_window, s_window, p_window = int(
                0.05 * sampling_rate), int(0.05 * sampling_rate), int(0.15 * sampling_rate)

            for i, r in enumerate(r_peaks):
                start_q, end_q = max(r - q_window, 0), r
                q_peaks.append(
                    np.argmin(filtered_signal[start_q:end_q]) + start_q)

                start_s, end_s = r, min(r + s_window, len(filtered_signal))
                s_peaks.append(
                    np.argmin(filtered_signal[start_s:end_s]) + start_s)

                start_p, end_p = max(q_peaks[-1] - p_window, 0), q_peaks[-1]
                p_peaks.append(
                    np.argmax(filtered_signal[start_p:end_p]) + start_p)

                if i < len(r_peaks) - 1:
                    next_r = r_peaks[i+1]
                else:
                    next_r = len(filtered_signal)
                t_offset, margin = int(
                    0.02 * sampling_rate), int(0.05 * sampling_rate)
                start_t = s_peaks[-1] + t_offset if s_peaks else 0
                end_t = max(next_r - margin, start_t + 1)
                t_peaks.append(
                    np.argmax(filtered_signal[start_t:end_t]) + start_t)

            # Tracé du signal ECG avec les pics détectés
            plt.figure(figsize=(12, 6))
            plt.plot(time, filtered_signal,
                     label="ECG Filtré (BioSPPy)", color='black')
            plt.scatter(time[r_peaks], filtered_signal[r_peaks],
                        color='red', label="R-peaks")
            plt.scatter(time[q_peaks], filtered_signal[q_peaks],
                        color='green', label="Q-peaks")
            plt.scatter(time[s_peaks], filtered_signal[s_peaks],
                        color='magenta', label="S-peaks")
            plt.scatter(time[p_peaks], filtered_signal[p_peaks],
                        color='cyan', label="P-peaks")
            plt.scatter(time[t_peaks], filtered_signal[t_peaks],
                        color='yellow', label="T-peaks")

            plt.xlabel("Temps (s)")
            plt.ylabel("Amplitude")
            plt.title(
                f"Détection des ondes PQRST avec BioSPPy ({start_time}s - {end_time}s)")
            plt.legend()
            plt.show()

            # Affichage des indices détectés
            print("Detected R-peaks indices:", r_peaks)
            print("Detected Q-peaks indices:", q_peaks)
            print("Detected S-peaks indices:", s_peaks)
            print("Detected P-peaks indices:", p_peaks)
            print("Detected T-peaks indices:", t_peaks)
