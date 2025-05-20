import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


class TrendExtractor:
    """
    Classe permettant d’extraire une tendance lente d’un signal physiologique (ex. : signal cardiaque).
    Trois méthodes sont disponibles :
        - Moyenne glissante centrée
        - Spline cubique lissée
        - Combinaison des deux
    """

    def __init__(self, signal, time):
        """
        Args:
            signal (np.ndarray) : Signal brut
            time (np.ndarray)   : Axe temporel associé
        """
        self.signal = signal
        self.time = time
        self.trend = None  # Stocke la dernière tendance extraite

    def extract_rolling_mean(self, window_size=1001):
        """
        Calcule la tendance via une moyenne glissante centrée, avec padding aux bords.

        Args:
            window_size (int): Taille de la fenêtre (impair conseillé)

        Returns:
            np.ndarray : signal de tendance
        """
        if window_size % 2 == 0:
            window_size += 1  # S'assurer que la fenêtre est impaire

        half_win = window_size // 2

        # Extension du signal en miroir pour éviter les effets de bord
        padded = np.pad(self.signal, (half_win, half_win), mode='reflect')

        # Convolution centrée (mode='valid' sur le signal étendu)
        trend = np.convolve(padded, np.ones(
            window_size) / window_size, mode='valid')

        self.trend = trend
        return trend

    def extract_spline(self, smooth_factor=1e7):
        """
        Calcule la tendance via une spline cubique lissée.

        Args:
            smooth_factor (float): Paramètre de lissage de la spline (plus grand = plus lisse)

        Returns:
            np.ndarray : signal de tendance
        """
        spline = UnivariateSpline(self.time, self.signal, s=smooth_factor)
        self.trend = spline(self.time)
        return self.trend

    def extract_combined(self, rolling_window=1001, smooth_factor=1e7):
        """
        Calcule une tendance combinée (moyenne glissante + spline).

        Args:
            rolling_window (int)   : Taille de la moyenne glissante
            smooth_factor (float)  : Facteur de lissage de la spline

        Returns:
            np.ndarray : signal de tendance combinée
        """
        trend_roll = self.extract_rolling_mean(window_size=rolling_window)
        trend_spline = self.extract_spline(smooth_factor=smooth_factor)

        combined = 0.5 * trend_roll + 0.5 * trend_spline
        self.trend = combined
        return combined

    def plot_trend(self, label="Tendance", show=True, save_path=None):
        """
        Affiche le signal original et la tendance extraite.

        Args:
            label (str)         : Légende pour la tendance
            show (bool)         : Afficher la figure
            save_path (str|None): Chemin pour enregistrer l’image
        """
        plt.figure(figsize=(14, 4))
        plt.plot(self.time, self.signal, label="Signal original", alpha=0.5)

        if self.trend is not None:
            plt.plot(self.time, self.trend, label=label, color='red')

        plt.title("Extraction de la tendance")
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
