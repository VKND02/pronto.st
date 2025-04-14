import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Paramètres ===
filepath = "data/data1/Sansinjection.txt"  # Ton fichier
start_time = 0       # début en secondes
end_time = 30        # fin en secondes
interval_ms = 5      # intervalle entre chaque mesure

# === Chargement brut ===
df = pd.read_csv(filepath, sep='\t', header=None,
                 encoding='ISO-8859-1', engine="python")

# Affecter les noms de colonnes (si 8 colonnes max)
df.columns = ["Time", "BP", "Av BP", "HR", "D",
              "HR2", "Comment", "Extra"][:df.shape[1]]

# Supprimer les lignes contenant du texte dans des colonnes numériques
for col in ["BP", "Av BP", "HR", "D", "HR2"]:
    df[col] = pd.to_numeric(df[col].astype(
        str).str.replace(",", "."), errors="coerce")

# Supprimer les colonnes inutiles
df.drop(columns=[c for c in ["Comment", "Extra"]
        if c in df.columns], inplace=True)

# Supprimer les lignes incomplètes
df.dropna(inplace=True)

# Recalcul de la colonne "Time"
df["Time"] = np.arange(0, len(df)) * (interval_ms / 1000)
min_time, max_time = df["Time"].min(), df["Time"].max()
print(f"📌 Temps total disponible : {min_time:.2f}s à {max_time:.2f}s")

# Filtrer la fenêtre de temps
df_plot = df[(df["Time"] >= start_time) & (df["Time"] <= end_time)]

# === Tracer les signaux ===
cols_to_plot = ["BP", "Av BP", "HR", "D", "HR2"]

for col in cols_to_plot:
    plt.figure(figsize=(14, 4))
    plt.plot(df_plot["Time"], df_plot[col], label=col)
    plt.title(f"{col} - Signal brut")
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
