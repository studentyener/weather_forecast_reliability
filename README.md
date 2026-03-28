# Analyse de la fiabilité des prévisions météo

Petit projet personnel d'évaluation des prévisions météo sur quelques villes françaises. L'idée de départ est simple : est-ce qu'on peut vraiment faire confiance à une prévision à 5 jours ?

---

## Pourquoi ce projet

J'ai souvent pris des décisions en fonction de la météo annoncée — weekends, sorties, déplacements — pour me retrouver avec une météo complètement différente de ce qui était prévu. Ça m'a donné envie de mesurer concrètement l'écart entre ce que les modèles prévoient et ce qui se passe réellement.

C'est aussi l'occasion de travailler sur un pipeline de données complet, de la collecte à la visualisation, avec quelque chose de concret et facile à expliquer.

---

## Ce que fait le projet

À partir d'un panel de 8 villes françaises, le projet :

- collecte des prévisions météo via l'API OpenWeatherMap (ou génère des données synthétiques si pas de clé)
- simule un historique de 30 jours de prévisions vs observations réelles
- calcule des indicateurs de fiabilité : MAE, RMSE, biais, indice composite
- classe les villes selon la fiabilité de leurs prévisions
- exporte les résultats en CSV et les graphiques en HTML interactif

---

## Résultats obtenus

Sur les 8 villes du panel, les erreurs de prévision restent contenues (MAE < 1.6 °C), mais les différences entre villes sont réelles.

| Rang | Ville       | Score /100 | MAE °C | RMSE °C | Biais  |
|------|-------------|-----------|--------|---------|--------|
| 1    | Lyon        | 65.3      | 1.04   | 1.33    | −0.34  |
| 2    | Paris       | 60.9      | 1.24   | 1.57    | +0.14  |
| 3    | Toulouse    | 59.2      | 1.30   | 1.59    | +0.19  |
| 4    | Nantes      | 57.1      | 1.31   | 1.71    | −0.28  |
| 5    | Strasbourg  | 55.1      | 1.43   | 1.77    | +0.18  |
| 6    | Marseille   | 52.1      | 1.56   | 1.91    | +0.09  |
| 7    | Lille       | 51.1      | 1.36   | 1.88    | +0.70  |
| 8    | Nice        | 50.4      | 1.55   | 1.98    | +0.24  |

Ce qui ressort : **Lyon est la ville la mieux prévue** du panel. **Lille affiche le biais le plus fort** (+0.70 °C) : les températures y sont systématiquement surestimées. Nice et Marseille ont les MAE les plus élevées malgré un biais faible, ce qui suggère une variabilité importante autour d'une prévision centrale correcte.

---

## Structure

```
weather_forecast_reliability/
├── README.md
├── PROJECT_NOTE_PERSONNELLE.md
├── requirements.txt
├── run_project.sh
├── launch_jupyter.sh
├── weather_forecast_final.ipynb
├── src/
│   ├── config.py
│   ├── data_collection.py
│   ├── analysis.py
│   ├── visualization.py
│   └── main.py
├── data/
│   └── processed/
└── outputs/
```

---

## Installation

```bash
git clone https://github.com/studentyener/weather_forecast_reliability.git
cd weather_forecast_reliability

python3 -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

---

## Lancer le projet

**Via script (terminal) :**
```bash
./run_project.sh
```

**Via Jupyter :**
```bash
./launch_jupyter.sh
```
Puis ouvrir `weather_forecast_final.ipynb` et exécuter toutes les cellules.

**Avec une vraie clé API OpenWeatherMap :**
```bash
export OPENWEATHER_API_KEY="ta_cle_ici"
./run_project.sh
```
Sans clé, le projet tourne quand même en mode synthétique — les résultats sont reproductibles à l'identique.

---

## Fichiers générés

Après exécution, dans `data/processed/` :
- `villes.csv` — panel des villes avec coordonnées
- `coords.csv` — coordonnées utilisées pour les appels API
- `forecasts.csv` — prévisions (réelles ou synthétiques)
- `historique.csv` — historique 30 jours prévision vs observation
- `metrics.csv` — MAE, RMSE, biais, indice de fiabilité par ville
- `city_scores.csv` — classement final par score composite

Dans `outputs/` :
- `mae_horizon.html` — graphique interactif MAE par ville
- `heatmap_scores.html` — heatmap des indicateurs

---

## Dépendances

Python 3.9+, pandas, numpy, plotly, requests, scipy, jupyter.
Voir `requirements.txt` pour les versions exactes.

---

## Auteur

YENER Dogukan — M2 DS2E, Université de Strasbourg, 2025–2026  
GitHub : [github.com/studentyener](https://github.com/studentyener)
