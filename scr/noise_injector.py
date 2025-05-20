import numpy as np
from scipy.ndimage import gaussian_filter1d


class NoiseInjector:
    """
    Classe pour injecter un bruit contrôlé dans les différents composants du signal physiologique :
    - R-R intervals (largeur des battements)
    - Amplitudes (hauteur des battements)
    - Tendance lente (modulation globale)

    Le bruit est gaussien et lissé pour simuler des variations naturelles non brutales.
    """

    def __init__(self, seed=None):
        """
        Args:
            seed (int ou None) : Graine pour rendre le bruit reproductible
        """
        self.rng = np.random.default_rng(seed)

    def _smoothed_noise(self, length, std=0.02, smoothing_sigma=3):
        """
        Génère un bruit gaussien 1D lissé pour simuler une perturbation naturelle et douce.

        Args:
            length (int): Taille du vecteur de bruit
            std (float): Écart-type du bruit
            smoothing_sigma (int): Lissage par filtre gaussien (plus grand = plus lisse)

        Returns:
            np.ndarray : Bruit lissé
        """
        noise = self.rng.normal(0, std, size=length)
        return gaussian_filter1d(noise, sigma=smoothing_sigma)

    def add_noise_to_rr(self, rr_intervals, noise_std=0.02, smoothing_sigma=3):
        """
        Ajoute un bruit réaliste aux intervalles R-R pour perturber les largeurs des battements.

        Args:
            rr_intervals (np.ndarray): Durées des battements (en secondes)
            noise_std (float): Intensité du bruit
            smoothing_sigma (int): Lissage du bruit

        Returns:
            np.ndarray : Intervalles bruités, bornés pour éviter des valeurs trop faibles
        """
        noise = self._smoothed_noise(
            len(rr_intervals), std=noise_std, smoothing_sigma=smoothing_sigma)
        noisy_rr = rr_intervals + noise
        # Empêche les battements irréalistes
        return np.clip(noisy_rr, a_min=0.3, a_max=None)

    def add_noise_to_amplitudes(self, amplitudes, noise_std=0.1, smoothing_sigma=3):
        """
        Applique un bruit multiplicatif lissé aux amplitudes locales (plus réaliste qu’un bruit additif).

        Args:
            amplitudes (np.ndarray): Amplitudes extraites (via enveloppe)
            noise_std (float): Écart-type du bruit relatif
            smoothing_sigma (int): Lissage du bruit

        Returns:
            np.ndarray : Amplitudes perturbées
        """
        noise = self._smoothed_noise(
            len(amplitudes), std=noise_std, smoothing_sigma=smoothing_sigma)
        noisy_amp = amplitudes * (1 + noise)
        return np.clip(noisy_amp, a_min=0.1, a_max=None)

    def add_noise_to_trend(self, trend, noise_std=0.05, smoothing_sigma=10):
        """
        Applique un bruit additif doux à la tendance lente, pour la rendre moins parfaitement lisse.

        Args:
            trend (np.ndarray): Vecteur de tendance
            noise_std (float): Écart-type du bruit additif
            smoothing_sigma (int): Degré de lissage

        Returns:
            np.ndarray : Tendance bruitée
        """
        noise = self._smoothed_noise(
            len(trend), std=noise_std, smoothing_sigma=smoothing_sigma)
        return trend + noise
