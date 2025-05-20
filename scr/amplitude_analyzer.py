import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, find_peaks
from scipy.interpolate import interp1d


class AmplitudeAnalyzer:
    """
    Classe dédiée à l’analyse de l’amplitude d’un signal cardiaque.
    Elle permet de calculer et visualiser différentes enveloppes du signal.

    Méthodes d’enveloppe :
        - Hilbert : amplitude instantanée via transformée analytique
        - Interpolation : enveloppes sup/inf via pics locaux
        - MinMax : fenêtre glissante locale avec max/min
    """

    def __init__(self, signal, time, sampling_rate=200):
        """
        Args:
            signal (np.ndarray)        : Signal brut (HR ou ECG)
            time (np.ndarray)          : Axe temporel
            sampling_rate (float)      : Fréquence d’échantillonnage en Hz (par défaut 200 Hz)
        """
        self.signal = signal
        self.time = time
        self.sampling_rate = sampling_rate

        self.envelope_hilbert = None
        self.envelope_interp = None
        self.envelope_minmax = None

    def compute_hilbert_envelope(self):
        """
        Calcule l’enveloppe via transformée de Hilbert (amplitude instantanée).
        """
        analytic_signal = hilbert(self.signal)
        self.envelope_hilbert = np.abs(analytic_signal)
        return self.envelope_hilbert

    def compute_interpolated_envelope(self, distance=20, prominence=0.1):
        """
        Enveloppe par interpolation linéaire entre maxima et minima locaux.

        Args:
            distance (int)    : Distance minimale entre pics
            prominence (float): Seuil de proéminence pour détection des pics

        Returns:
            Tuple[np.ndarray, np.ndarray] : enveloppe supérieure et inférieure
        """
        max_peaks, _ = find_peaks(
            self.signal, distance=distance, prominence=prominence)
        min_peaks, _ = find_peaks(-self.signal,
                                  distance=distance, prominence=prominence)

        # Sécuriser les bords
        if 0 not in max_peaks:
            max_peaks = np.insert(max_peaks, 0, 0)
        if len(self.signal) - 1 not in max_peaks:
            max_peaks = np.append(max_peaks, len(self.signal) - 1)

        if 0 not in min_peaks:
            min_peaks = np.insert(min_peaks, 0, 0)
        if len(self.signal) - 1 not in min_peaks:
            min_peaks = np.append(min_peaks, len(self.signal) - 1)

        x = np.arange(len(self.signal))
        upper = interp1d(
            max_peaks, self.signal[max_peaks], kind='linear', fill_value='extrapolate')(x)
        lower = interp1d(
            min_peaks, self.signal[min_peaks], kind='linear', fill_value='extrapolate')(x)

        self.envelope_interp = (upper, lower)
        return upper, lower

    def compute_minmax_envelope(self, window_size=200):
        """
        Enveloppe locale par fenêtre glissante (min et max locaux).

        Args:
            window_size (int) : Taille de la fenêtre (en nb d’échantillons)

        Returns:
            Tuple[np.ndarray, np.ndarray] : enveloppe supérieure et inférieure
        """
        n = len(self.signal)
        upper = np.zeros(n)
        lower = np.zeros(n)
        half_window = window_size // 2

        for i in range(n):
            start = max(0, i - half_window)
            end = min(n, i + half_window)
            upper[i] = np.max(self.signal[start:end])
            lower[i] = np.min(self.signal[start:end])

        self.envelope_minmax = (upper, lower)
        return upper, lower

    def analyze_envelope_amplitude(self, method="hilbert"):
        """
        Calcule les statistiques d’amplitude selon la méthode choisie.

        Args:
            method (str): "hilbert", "interp" ou "minmax"

        Returns:
            dict : Moyenne, écart-type, min et max d’amplitude
        """
        if method == "hilbert":
            if self.envelope_hilbert is None:
                self.compute_hilbert_envelope()
            amp = self.envelope_hilbert

        elif method == "interp":
            if self.envelope_interp is None:
                self.compute_interpolated_envelope()
            upper, lower = self.envelope_interp
            amp = upper - lower

        elif method == "minmax":
            if self.envelope_minmax is None:
                self.compute_minmax_envelope()
            upper, lower = self.envelope_minmax
            amp = upper - lower

        else:
            raise ValueError(f"Méthode inconnue : {method}")

        return {
            "mean_amplitude": np.mean(amp),
            "std_amplitude": np.std(amp),
            "min_amplitude": np.min(amp),
            "max_amplitude": np.max(amp)
        }

    def plot_envelope(self, method="hilbert", show=True, save_path=None):
        """
        Affiche le signal et son enveloppe (méthode au choix).

        Args:
            method (str)       : Méthode d’enveloppe à tracer ("hilbert", "interp", "minmax")
            show (bool)        : Afficher directement la figure (par défaut True)
            save_path (str|None): Chemin de sauvegarde optionnel
        """
        plt.figure(figsize=(14, 4))
        plt.plot(self.time, self.signal, label="Signal", alpha=0.6)

        if method == "hilbert":
            if self.envelope_hilbert is None:
                self.compute_hilbert_envelope()
            plt.plot(self.time, self.envelope_hilbert,
                     color="red", label="Enveloppe (Hilbert)")

        elif method == "interp":
            if self.envelope_interp is None:
                self.compute_interpolated_envelope()
            upper, lower = self.envelope_interp
            plt.plot(self.time, upper, color="red", label="Enveloppe sup.")
            plt.plot(self.time, lower, color="blue", label="Enveloppe inf.")

        elif method == "minmax":
            if self.envelope_minmax is None:
                self.compute_minmax_envelope()
            upper, lower = self.envelope_minmax
            plt.plot(self.time, upper, color="orange", label="Enveloppe sup.")
            plt.plot(self.time, lower, color="green", label="Enveloppe inf.")
        else:
            raise ValueError(f"Méthode d'enveloppe inconnue : {method}")

        plt.title(f"Enveloppe du signal ({method})")
        plt.xlabel("Temps (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.legend()

        if save_path:
            plt.savefig(save_path)
        if show:
            plt.show()
        else:
            plt.close()
