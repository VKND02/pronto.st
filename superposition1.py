import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# Signal ECG parfait à 200 Hz, 254 s, 200 bpm
sampling_rate = 200
duration_seconds = 254
heart_rate = 200
beats_per_second = heart_rate / 60
beat_duration = 1 / beats_per_second
samples_per_beat = int(sampling_rate * beat_duration)
n_beats = int(duration_seconds * beats_per_second)

# Générer un motif ECG idéal
def generate_ecg_beat(samples_per_beat):
    t = np.linspace(0, samples_per_beat / sampling_rate, samples_per_beat, endpoint=False)
    ecg = np.zeros_like(t)

    def gaussian(t, mu, sigma, amp):
        return amp * np.exp(-0.5 * ((t - mu) / sigma)**2)

    ecg += gaussian(t, 0.2 * beat_duration, 0.025 * beat_duration, 0.1)
    ecg += gaussian(t, 0.35 * beat_duration, 0.01 * beat_duration, -0.15)
    ecg += gaussian(t, 0.4 * beat_duration, 0.012 * beat_duration, 1.0)
    ecg += gaussian(t, 0.45 * beat_duration, 0.01 * beat_duration, -0.25)
    ecg += gaussian(t, 0.6 * beat_duration, 0.05 * beat_duration, 0.35)
    return ecg

ecg_beat = generate_ecg_beat(samples_per_beat)
ecg_full = np.tile(ecg_beat, n_beats)


# Charger le fichier de tendance
df = pd.read_csv("Adrenaline.txt", sep="\t", header=None)
df[1] = df[1].astype(str).str.replace(",", ".").astype(float)

# Appliquer une moyenne mobile pour extraire la tendance
df["ultra_smooth"] = df[1].rolling(window=1100, center=True).mean()
df_clean = df.dropna(subset=["ultra_smooth"])

# Extraire la tendance et l'ajuster à la longueur du signal ECG
trend_extracted = df_clean["ultra_smooth"].values
if len(trend_extracted) > len(ecg_full):
    trend_extracted = trend_extracted[:len(ecg_full)]
#on complete en ajoutant par defaut la deniere valeur de trend_extracted
elif len(trend_extracted) < len(ecg_full):
    last_val = trend_extracted[-1]
    trend_extracted = np.pad(trend_extracted, (0, len(ecg_full) - len(trend_extracted)), constant_values=last_val)

# Normalisation de la tendance pour la transformer en facteur multiplicatif
trend_normalise = (trend_extracted - np.min(trend_extracted)) / (np.max(trend_extracted) - np.min(trend_extracted))
trend_scaled = trend_normalise * 2  # mise à l'échelle

# Appliquer cette tendance extraite au signal ECG synthétique
ecg_superposed = ecg_full  + trend_scaled
time = np.arange(len(ecg_full)) / sampling_rate


# Sauvegarde du fichier résultant
df_result = pd.DataFrame({"Time (s)": time, "ECG_with_extracted_trend": ecg_superposed})
csv_final_path = "/mnt/data/ecg_synthetique_with_extracted_trend.csv"
df_result.to_csv(csv_final_path, index=False)

# Affichage (premiers instants du signal)
plt.figure(figsize=(12, 3))
#modifier x dans time[:x] pour visualiser le signal sur une echelle de temps différente
plt.plot(time[:30000], ecg_superposed[:30000], label="ECG × tendance extraite", color="darkblue")

plt.title("ECG synthétique modulé par tendance extraite (150 premières secondes)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

csv_final_path