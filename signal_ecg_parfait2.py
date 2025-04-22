import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Paramètres demandés ---
sampling_rate = 200  # Hz
duration_seconds = 254
heart_rate = 200  # bpm

# Calculs
beats_per_second = heart_rate / 60
beat_duration = 1 / beats_per_second  # durée d'un battement en secondes
samples_per_beat = int(sampling_rate * beat_duration)
n_beats = int(duration_seconds * 3.3)

# Fonction pour générer un battement ECG
def generate_ecg_beat(sampling_rate, samples_per_beat):
    t = np.linspace(0, samples_per_beat / sampling_rate, samples_per_beat, endpoint=False)
    ecg = np.zeros_like(t)

    def gaussian(t, mu, sigma, amp):
        return amp * np.exp(-0.5 * ((t - mu) / sigma) ** 2)

    # Positions relatives (ajustées à beat_duration)
    beat_duration = samples_per_beat / sampling_rate
    ecg += gaussian(t, 0.2 * beat_duration, 0.025 * beat_duration, 0.1)   # P
    ecg += gaussian(t, 0.35 * beat_duration, 0.01 * beat_duration, -0.15) # Q
    ecg += gaussian(t, 0.4 * beat_duration, 0.012 * beat_duration, 1.0)   # R
    ecg += gaussian(t, 0.45 * beat_duration, 0.01 * beat_duration, -0.25) # S
    ecg += gaussian(t, 0.6 * beat_duration, 0.05 * beat_duration, 0.35)   # T

    return ecg

# Générer le signal complet
beat = generate_ecg_beat(sampling_rate, samples_per_beat)
ecg_full = np.tile(beat, n_beats)
time = np.arange(len(ecg_full)) / sampling_rate

# Sauvegarde en CSV
df = pd.DataFrame({"Time (s)": time, "ECG": ecg_full})
csv_path = "/mnt/data/ecg_synthetique_254s_200bpm.csv"
df.to_csv(csv_path, index=False)

# Affichage
plt.figure(figsize=(12, 3))
plt.plot(time[:10000], ecg_full[:10000])  # affichage d’un extrait (50 secondes)
plt.title("Extrait d'ECG synthétique (200 bpm, 200 Hz)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.show()

csv_path
