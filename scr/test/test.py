## explications 


# fonction .rolling(window,center= True).mean()"

"Crée courbe lissée à partir du signal brut, en utilisant une moyenne mobile centrée "
"sur 1100 points, ce qui permet d’isoler la tendance de fond du signal."
"ultra_smooth(t) = sum(x[i], for i in [t-550,t+550])"

"Aux bords, où il y a moins de points — ça crée des NaN d'ou la suggestion plus haut "
"d'ajouter artificiellement des points"


#fonction UnivariateSpline
"from scipy.interpolate import UnivariateSpline"
" spline = UnivariateSpline(x, y, s=0) "

"x : vecteur des abscisses (croissant strictement)"

"y : valeurs à approximer"

"s : paramètre de lissage/ bruit, fixé ici à O puisqu'on a déjà retiré de bruit"



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# --- 1. Charger et nettoyer les données ---
df = pd.read_csv("Adrenaline.txt", sep="\t", header=None)
df[1] = df[1].astype(str).str.replace(",", ".").astype(float)
df["time"] = pd.date_range(start='2022-01-01', periods=len(df), freq='s')
df["ultra_smooth"] = df[1].rolling(window=1100, center=True).mean()

# --- 2. Supprimer les valeurs NaN créées par le rolling ---
df_clean = df.dropna(subset=["ultra_smooth"])
x = np.arange(len(df_clean))
y = df_clean["ultra_smooth"].values

# --- 3. Appliquer un spline cubique ---
# s=0 => interpolation exacte (overfit parfait)
spline = UnivariateSpline(x, y, s=1)
y_spline = spline(x)

# --- 4. Tracer le résultat ---
plt.figure(figsize=(12, 5))
plt.plot(df_clean["time"], y, label="trend extration", color='darkred', linewidth=2)
plt.plot(df_clean["time"], y_spline, label="Fit spline ", color='green', linestyle='--')
plt.title("Overfitting de la tendance avec Spline")
plt.xlabel("Temps")
plt.ylabel("Valeur")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

"Remarques "
" on aurait pu interpoler avec :"
"       - interp1d du module scipy qui colle exactement à la courbe ( pb is il y a du bruit)"
"       "
"       - GPR : processus sto qui colle bien " 

"Pour optimiser la précsion de la fenetre qui effectue un moyenne arithmétique"
" sur les 550 valeurs avant et après, pour les valeurs extremes on pourrait rajouter"
"artificiellement des points"

"CCL : on extrait effectivement la tendance et le processus utilisé est convainquant."
"        Néanmoins quand on zoom bcp localement on voit des pics si en pratique la superposition avec les "
"         autres paramètres donne un résultat peu réaliste, on pourrait "
"           effectué à nouveau ce processus sur la courbe obtenue pour éliminer completment les pics "


#print("infos supplémentaires")
# Points de rupture (noeuds)
#print("Knots (noeuds) :", spline.get_knots())

# Coefficients spline
#print("Coefficients :", spline.get_coeffs())

# Degré du spline
#print("Degré :", spline.get_k()) 

