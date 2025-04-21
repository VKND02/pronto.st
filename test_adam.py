import pandas as pd
import matplotlib.pyplot as plt

# Lire le fichier (sans noms de colonnes fixes)
df = pd.read_csv("Adrenaline.txt", sep="\t", header=None)

# Nettoyer la colonne 1 (Signal1) : remplacer virgule -> point + float
df[1] = df[1].astype(str).str.replace(",", ".").astype(float)
df["time"] = pd.date_range(start='2022-01-01', periods=len(df), freq='s')

# Appliquer une moyenne mobile très large pour une tendance ultra lissée
df["ultra_smooth"] = df[1].rolling(window=1000, center=True).mean()

# Exporter la tendance dans un CSV
df[["time", 1, "ultra_smooth"]].to_csv("tendance_ultra_lissee.csv", index=False)

# Affichage
plt.figure(figsize=(12, 4))
plt.plot(df["time"], df[1], label="Signal brut", color='lightblue', alpha=0.3)
plt.plot(df["time"], df["ultra_smooth"], label="Tendance ultra lissée", color='darkred', linewidth=2)
plt.title("Tendance ultra lissée du signal")
plt.xlabel("Temps")
plt.ylabel("Valeur")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

