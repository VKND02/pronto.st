import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class DataLoader:
    """
    Classe permettant de charger, nettoyer, découper et visualiser des données physiologiques.

    Attributs :
        filepath (str)         : Chemin vers le fichier de données (.txt)
        interval_ms (float)    : Intervalle d'échantillonnage en millisecondes (par défaut 5 ms → 200 Hz)
        data (pd.DataFrame)    : Données brutes chargées et nettoyées
    """

    def __init__(self, filepath, interval_ms=5):
        self.filepath = filepath
        self.interval_ms = interval_ms
        self.data = None
        self.columns_full = ["Time", "HR", "Av BP",
                             "BP", "D", "BP2", "Comment", "Extra"]
        self.useful_cols = ["HR", "Av BP", "BP", "D", "BP2"]

    def load(self):
        """
        Charge le fichier texte, nettoie les colonnes numériques,
        supprime les colonnes inutiles et ajoute une colonne temporelle.

        Returns:
            pd.DataFrame : Données nettoyées avec colonne "Time"
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Fichier introuvable : {self.filepath}")

        # Chargement brut
        df = pd.read_csv(self.filepath, sep='\t', header=None,
                         encoding='ISO-8859-1', engine='python')

        # Attribution des noms de colonnes selon la largeur
        df.columns = self.columns_full[:df.shape[1]]

        # Conversion des colonnes utiles (avec "," en ".")
        for col in self.useful_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(
                    str).str.replace(",", "."), errors='coerce')

        # Suppression des colonnes non pertinentes
        df.drop(columns=[c for c in ["Comment", "Extra"]
                if c in df.columns], inplace=True)

        # Suppression des lignes incomplètes
        df.dropna(inplace=True)

        # Génération d'une colonne temporelle
        df["Time"] = np.arange(0, len(df)) * (self.interval_ms / 1000)

        self.data = df.reset_index(drop=True)
        return self.data

    def crop_time_range(self, start_time, end_time):
        """
        Découpe une plage temporelle spécifique dans les données chargées.

        Args:
            start_time (float) : Temps de début en secondes
            end_time (float)   : Temps de fin en secondes

        Returns:
            pd.DataFrame : Données restreintes à la plage choisie
        """
        if self.data is None:
            raise ValueError(
                "⚠️ Utilisez .load() avant de découper une plage.")

        min_time, max_time = self.data["Time"].min(), self.data["Time"].max()
        if start_time < min_time or end_time > max_time:
            raise ValueError(
                f"Plage temporelle invalide : {start_time}s → {end_time}s hors bornes [{min_time}s → {max_time}s]")

        return self.data[
            (self.data["Time"] >= start_time) & (self.data["Time"] <= end_time)
        ].reset_index(drop=True)

    def plot(self, df_crop, save_path=None, show=True):
        """
        Affiche (et optionnellement enregistre) chaque signal contenu dans df_crop.

        Args:
            df_crop (pd.DataFrame) : Données à tracer (issues de crop_time_range)
            save_path (str)        : Dossier dans lequel enregistrer les figures (facultatif)
            show (bool)            : Affiche les figures à l’écran (True) ou non (False)
        """
        time_col = "Time"
        signal_cols = [col for col in df_crop.columns if col != time_col]

        for col in signal_cols:
            plt.figure(figsize=(12, 4))
            plt.plot(df_crop[time_col], df_crop[col], label=col)
            plt.title(f"Signal brut - {col}")
            plt.xlabel("Temps (s)")
            plt.ylabel("Amplitude")
            plt.grid(True)
            plt.legend()

            if save_path:
                filename = f"{save_path}/{col}_raw_plot.png"
                plt.savefig(filename)
                print(f"Figure enregistrée : {filename}")

            if show:
                plt.show()
            else:
                plt.close()
