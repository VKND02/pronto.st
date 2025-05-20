import numpy as np
import matplotlib.pyplot as plt


class SignalGenerator:
    """
    Classe permettant de générer un signal cardiaque synthétique en reproduisant des battements de cœur
    à partir de séquences de durées R-R et d’amplitudes extraites du signal réel.

    Fonctionnalités :
    - Génération de battements ECG sous forme de sommes de gaussiennes
    - Construction du signal complet battement par battement
    - Application d'une tendance lente
    - Visualisation zoomable
    """

    def __init__(self, sampling_rate=200):
        """
        Args:
            sampling_rate (int): Taux d’échantillonnage en Hz (par défaut : 200 Hz)
        """
        self.sampling_rate = sampling_rate
        self.signal_flat = None        # Signal sans tendance
        self.signal_final = None       # Signal final avec tendance ajoutée
        self.time = None               # Axe temporel associé

    def generate_ecg_beat(self, duration, amplitude=1.0):
        """
        Génère un battement ECG synthétique sous forme de somme de gaussiennes : ondes P, Q, R, S, T.

        Args:
            duration (float): Durée du battement en secondes (issue de l’intervalle R-R)
            amplitude (float): Amplitude globale du battement

        Returns:
            tuple (ecg, r_index):
                - ecg (np.ndarray) : Signal du battement
                - r_index (int)    : Index du pic R dans le battement
        """
        t = np.linspace(0, duration, int(
            self.sampling_rate * duration), endpoint=False)
        ecg = np.zeros_like(t)

        def gaussian(t, mu, sigma, amp):
            return amp * np.exp(-0.5 * ((t - mu) / sigma) ** 2)

        # Construction du battement avec les ondes
        ecg += gaussian(t, 0.20 * duration, 0.025 *
                        duration,  0.1 * amplitude)   # Onde P
        ecg += gaussian(t, 0.35 * duration, 0.010 *
                        duration, -0.2 * amplitude)   # Onde Q
        ecg += gaussian(t, 0.40 * duration, 0.012 *
                        duration,  0.7 * amplitude)   # Onde R
        ecg += gaussian(t, 0.45 * duration, 0.010 *
                        duration, -0.3 * amplitude)   # Onde S
        ecg += gaussian(t, 0.60 * duration, 0.050 *
                        duration,  0.2 * amplitude)   # Onde T

        r_index = np.argmax(ecg)
        return ecg, r_index

    def tile_signal_from_arrays(self, rr_intervals, amplitudes):
        """
        Construit un signal complet en assemblant des battements ECG générés à partir des durées R-R
        et des amplitudes extraites.

        Args:
            rr_intervals (np.ndarray): Tableau des intervalles R-R (en secondes)
            amplitudes (np.ndarray)  : Tableau des amplitudes correspondantes

        Returns:
            np.ndarray : Signal ECG synthétique sans tendance
        """
        signal = []
        r_peak_positions = []
        last_r_global = 0

        for rr, amp in zip(rr_intervals, amplitudes):
            beat, r_index = self.generate_ecg_beat(duration=rr, amplitude=amp)

            start_index = last_r_global - r_index
            if start_index < 0:
                beat = beat[-start_index:]
                start_index = 0

            if len(signal) < start_index:
                signal += [0] * (start_index - len(signal))

            signal += list(beat)
            last_r_global = start_index + r_index
            r_peak_positions.append(last_r_global)

        self.signal_flat = np.array(signal)
        self.time = np.arange(len(self.signal_flat)) / self.sampling_rate
        return self.signal_flat

    def apply_trend(self, trend_array):
        """
        Ajoute une tendance lente au signal synthétique.

        Args:
            trend_array (np.ndarray): Tendance extraite du signal réel

        Returns:
            np.ndarray : Signal final avec tendance ajoutée
        """
        if len(trend_array) < len(self.signal_flat):
            trend_array = np.pad(trend_array, (0, len(
                self.signal_flat) - len(trend_array)), mode='edge')
        elif len(trend_array) > len(self.signal_flat):
            trend_array = trend_array[:len(self.signal_flat)]

        self.signal_final = self.signal_flat + trend_array
        return self.signal_final

    def plot(self, zoom_start=None, zoom_end=None, title=""):
        """
        Affiche le signal généré (complet ou zoomé sur une plage donnée).

        Args:
            zoom_start (float): Temps de début du zoom (en secondes)
            zoom_end (float)  : Temps de fin du zoom (en secondes)
            title (str)       : Titre du graphique
        """
        if self.time is None or self.signal_final is None:
            print("Signal non généré.")
            return

        t = self.time
        s = self.signal_final

        if zoom_start is not None and zoom_end is not None:
            mask = (t >= zoom_start) & (t <= zoom_end)
            t = t[mask]
            s = s[mask]

        plt.figure(figsize=(14, 4))
        plt.plot(t, s, label="Signal généré")
        plt.title(title)
        plt.xlabel("Temps (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_custom_signal(self, signal, time, zoom_start=None, zoom_end=None, title="Signal généré (custom)"):
        """
        Affiche n'importe quel signal donné avec son axe temporel (utile pour les signaux bruités ou alternatifs).

        Args:
            signal (np.ndarray): Signal à afficher
            time (np.ndarray)  : Axe temporel associé
            zoom_start (float) : Zoom début
            zoom_end (float)   : Zoom fin
            title (str)        : Titre de la figure
        """
        if signal is None or time is None:
            print("Signal ou temps manquant.")
            return

        t = time
        s = signal

        if zoom_start is not None and zoom_end is not None:
            mask = (t >= zoom_start) & (t <= zoom_end)
            t = t[mask]
            s = s[mask]

        plt.figure(figsize=(14, 4))
        plt.plot(t, s, label="Signal (custom)", color='darkred')
        plt.title(title)
        plt.xlabel("Temps (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
