import pandas as pd
import matplotlib.pyplot as plt

# Lire avec noms génériques
df = pd.read_csv("Adrenaline.txt", sep="\t", header=None)

# Nettoyage juste de la colonne qui t'intéresse
df[1] = df[1].astype(str).str.replace(",", ".").astype(float)

# Créer index temps
df["time"] = pd.date_range(start='2022-01-01', periods=len(df), freq='s')

# Lissage
df["smooth"] = df[1].rolling(window=300, center=True).mean()

# Export CSV
df[["time", 1, "smooth"]].to_csv("signal_lisse.csv", index=False)

# Affichage
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.plot(df["time"], df[1], label="Signal brut", color='lightblue', alpha=0.4)
plt.plot(df["time"], df["smooth"], label="Lissé", color='red')
plt.legend()
plt.grid(True)
plt.title("Tendance centrale (Signal1)")
plt.tight_layout()
plt.show()
