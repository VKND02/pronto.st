import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Adrenaline.txt", sep="\t", header=None)
df[1] = df[1].astype(str).str.replace(",", ".").astype(float)
df["time"] = pd.date_range(start='2022-01-01', periods=len(df), freq='s')
df["ultra_smooth"] = df[1].rolling(window=1000, center=True).mean()

# Nettoyer les NaN
df_clean = df.dropna(subset=["ultra_smooth"])

# Axe x = secondes depuis le début (entiers)
x = np.arange(len(df_clean))
y = df_clean["ultra_smooth"].values

# ⚠️ Overfitting très fin avec un polynôme de degré 100
deg = 50
coeffs = np.polyfit(x, y, deg=deg)
poly_func = np.poly1d(coeffs)
y_fit = poly_func(x)

# Affichage de l'équation
print(f"Équation polynomiale de degré {deg} :\n")
print(poly_func)

# Tracé
plt.figure(figsize=(12, 5))
plt.plot(df_clean["time"], y, label="Tendance ultra lissée", color='darkred', linewidth=2)
plt.plot(df_clean["time"], y_fit, label=f"Polynôme degré {deg}", color='green', linestyle='--')
plt.title(f"Overfitting très fin (polynôme degré {deg})")
plt.xlabel("Temps")
plt.ylabel("Valeur")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
