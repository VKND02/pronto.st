import pandas as pd


def get_ecg_duration(filepath):
    """
    Charge le fichier ECG et détermine sa durée totale en secondes.
    """
    try:
        df = pd.read_csv(filepath, sep='\t', header=None,
                         encoding='ISO-8859-1', engine='python')
        df.columns = ["Time", "BP", "Av BP", "HR", "D",
                      "HR2", "Comment", "Extra"][:df.shape[1]]

        df["Time"] = df["Time"].astype(str).str.replace(
            ',', '.', regex=True).astype(float)

        min_time = df["Time"].min()
        max_time = df["Time"].max()
        duration = max_time - min_time

        print(f"⏳ Durée totale du fichier : {duration:.2f} secondes")
        print(f"📌 Temps minimum : {min_time:.3f}s")
        print(f"📌 Temps maximum : {max_time:.3f}s")

        return duration

    except Exception as e:
        print(f"❌ Erreur lors du chargement du fichier : {e}")
        return None


if __name__ == "__main__":
    filepath = "data/data1/Sansinjection.txt"
    get_ecg_duration(filepath)
