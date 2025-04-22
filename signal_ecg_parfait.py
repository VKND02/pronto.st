import neurokit2 as nk
import matplotlib.pyplot as plt
from biosppy.signals import ecg as biosppy_ecg

# --- Paramètres ---
duration = 254             # secondes
sampling_rate = 200        # aps de 5ms 
heart_rate = 200           # battemlent de coeur typique d'un lapin

# --- 1. Générer un signal ECG parfait ---
ecg_clean = nk.ecg_simulate(duration=duration, sampling_rate=sampling_rate, heart_rate= heart_rate)

# --- 2. Analyse avec BioSPPy ---
out = biosppy_ecg.ecg(signal=ecg_clean, sampling_rate=sampling_rate, show=False)

# --- 3. Visualisation ---
time = [i / sampling_rate for i in range(len(ecg_clean))]

plt.figure(figsize=(14, 5))
plt.plot(time, ecg_clean, label="ECG synthétique", color="black")
plt.plot(out['rpeaks'] / sampling_rate, ecg_clean[out['rpeaks']], 'ro', label="R-peaks détectés")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.title("ECG Synthétique de 254 secondes à 200 Hz")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
