
"""
Script d'exemple pour charger et tracer un signal physiologique à partir des données PRONTO.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


def load_pronto_data(filepath):
    """
    Charge un fichier de données PRONTO et reconstruit un temps uniforme à 5ms.
    """
    df = pd.read_csv(filepath, sep="\t", header=None, encoding='ISO-8859-1')
    df.columns = ["Time", "BP", "Av BP", "HR", "D",
                  "HR2", "Comment", "Extra"][:df.shape[1]]

    # Nettoyage
    for col in ["Time", "BP", "Av BP", "HR", "D", "HR2"]:
        df[col] = df[col].astype(str).str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna()

    # Recalcul du temps (5 ms entre les points)
    df["Reconstructed_Time"] = [i * 0.005 for i in range(len(df))]

    return df


def plot_physio_signals(df):
    """
    Trace toutes les variables physiologiques disponibles.
    """
    plt.figure(figsize=(15, 10))
    for col in ["BP", "Av BP", "HR", "D", "HR2"]:
        plt.plot(df["Reconstructed_Time"], df[col], label=col)

    plt.xlabel("Temps (s)")
    plt.ylabel("Valeurs physiologiques")
    plt.title("Signaux bruts PRONTO")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    filepath = os.path.join("data", "data1", "Sansinjection.txt")
    df = load_pronto_data(filepath)
    plot_physio_signals(df)
