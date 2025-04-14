import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(filepath, interval_ms=5):
    df = pd.read_csv(filepath, sep='\t', header=None,
                     encoding='ISO-8859-1', engine="python")

    df.columns = ["Time", "BP", "Av BP", "HR", "D",
                  "HR2", "Comment", "Extra"][:df.shape[1]]

    for col in ["BP", "Av BP", "HR", "D", "HR2"]:
        df[col] = pd.to_numeric(df[col].astype(
            str).str.replace(",", "."), errors="coerce")

    df.drop(columns=[c for c in ["Comment", "Extra"]
            if c in df.columns], inplace=True)
    df.dropna(inplace=True)

    df["Time"] = np.arange(0, len(df)) * (interval_ms / 1000)
    return df


def plot_pronto_signals(df, start_time, end_time):
    df_plot = df[(df["Time"] >= start_time) & (df["Time"] <= end_time)]
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


if __name__ == "__main__":
    filepath = "data/data1/Sansinjection.txt"
    start_time = 0
    end_time = 30
    interval_ms = 5

    df = load_data(filepath, interval_ms=interval_ms)
    min_time, max_time = df["Time"].min(), df["Time"].max()
    print(f"📌 Temps total disponible : {min_time:.2f}s à {max_time:.2f}s")

    plot_pronto_signals(df, start_time, end_time)
