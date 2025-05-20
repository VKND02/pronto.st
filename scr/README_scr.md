# `scr/` — Modules Python du projet

Ce dossier contient les scripts Python organisés par étape du pipeline.  
Chaque fichier contient une **classe unique** bien documentée et testée dans `main.ipynb`.

---

## Liste des modules

- `data_loader.py` : chargement et découpage des données brutes (`DataLoader`)
- `peak_detector.py` : détection des R-peaks et calcul des intervalles R-R (`PeakDetector`)
- `amplitude_analyzer.py` : extraction de l’amplitude du signal via enveloppes (`AmplitudeAnalyzer`)
- `trend_extractor.py` : extraction d’une tendance lente (rolling mean, spline, mix) (`TrendExtractor`)
- `signal_generator.py` : génération de signaux synthétiques battement par battement (`SignalGenerator`)
- `noise_injector.py` : injection de bruit réaliste dans les R-R, amplitude ou tendance (`NoiseInjector`)

---

Chaque classe expose des méthodes principales (ex. `.plot()`, `.load()`, `.detect_r_peaks_manual()`, etc.) et peut être instanciée directement depuis le notebook principal.
