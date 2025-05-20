from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt


class PeakDetector:
    """
    Classe permettant de détecter les R-peaks dans un signal cardiaque (typiquement HR ou ECG),
    de calculer les intervalles R-R et de visualiser les résultats.

    Attributs :
        signal (np.ndarray)         : Signal brut (ex. HR)
        time (np.ndarray)           : Axe temporel associé
        sampling_rate (float)       : Fréquence d’échantillonnage (Hz), par défaut 200 Hz
        rpeaks (np.ndarray | None)  : Indices des R-peaks détectés
        rr_intervals (np.ndarray)   : Intervalles R-R calculés en secondes
    """

    def __init__(self, signal, time, sampling_rate=200):
        self.signal = signal
        self.time = time
        self.sampling_rate = sampling_rate
        self.rpeaks = None
        self.rr_intervals = None

    def detect_r_peaks_manual(self, distance_sec=0.4, prominence=3):
        """
        Détection manuelle des R-peaks à l’aide de SciPy (find_peaks).

        Args:
            distance_sec (float) : Durée minimale entre deux pics (en s)
            prominence (float)   : Proéminence minimale des pics (force du pic)

        Returns:
            rpeaks (np.ndarray)       : Indices des pics détectés
            rr_intervals (np.ndarray) : Liste des intervalles R-R en secondes
        """
        distance_samples = int(distance_sec * self.sampling_rate)
        self.rpeaks, _ = find_peaks(
            self.signal,
            distance=distance_samples,
            prominence=prominence
        )
        self.rr_intervals = np.diff(self.rpeaks) / self.sampling_rate
        return self.rpeaks, self.rr_intervals

    def get_rr_stats(self):
        """
        Calcule les statistiques de base sur les intervalles R-R.

        Returns:
            dict : Moyenne, écart-type, fréquence cardiaque moyenne, nombre de battements
        """
        if self.rr_intervals is None or len(self.rr_intervals) == 0:
            return {
                "mean_rr_interval_s": np.nan,
                "std_rr_interval_s": np.nan,
                "num_beats": 0,
                "heart_rate_bpm": np.nan
            }

        return {
            "mean_rr_interval_s": self.rr_intervals.mean(),
            "std_rr_interval_s": self.rr_intervals.std(),
            "num_beats": len(self.rr_intervals) + 1,  # n RR => n+1 battements
            "heart_rate_bpm": 60 / self.rr_intervals.mean()
        }

    def plot_r_peaks(self, zoom_start=None, zoom_end=None):
        """
        Affiche le signal brut avec les R-peaks détectés (entier ou sur une plage zoomée).

        Args:
            zoom_start (float) : Temps de début pour le zoom (en s)
            zoom_end (float)   : Temps de fin pour le zoom (en s)
        """
        t = self.time
        s = self.signal

        if zoom_start is not None and zoom_end is not None:
            mask = (t >= zoom_start) & (t <= zoom_end)
            t = t[mask]
            s = s[mask]
            rpeaks = self.rpeaks[
                (self.time[self.rpeaks] >= zoom_start) & (
                    self.time[self.rpeaks] <= zoom_end)
            ]
        else:
            rpeaks = self.rpeaks

        plt.figure(figsize=(14, 4))
        plt.plot(t, s, label="Signal brut", color='lightblue')
        plt.scatter(self.time[rpeaks], self.signal[rpeaks],
                    color='red', label='R-peaks')
        plt.title("Détection des R-peaks (manuel SciPy)")
        plt.xlabel("Temps (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_rr_intervals(self):
        """
        Affiche la série temporelle des intervalles R-R détectés (durée entre battements).
        """
        if self.rr_intervals is None:
            print("RR intervals non disponibles.")
            return

        plt.figure(figsize=(12, 3))
        plt.plot(self.rr_intervals, marker='o')
        plt.title("Intervalles R-R (durée entre battements)")
        plt.xlabel("Index")
        plt.ylabel("Durée (s)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def get_rpeaks_and_intervals(self):
        """
        Accès rapide aux R-peaks et intervalles R-R (utile dans main).

        Returns:
            Tuple[np.ndarray, np.ndarray] : rpeaks et rr_intervals
        """
        return self.rpeaks, self.rr_intervals
