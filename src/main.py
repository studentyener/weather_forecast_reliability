from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from data_collection import build_cities_df, build_coords_df, collect_forecasts
from analysis import build_synthetic_history, compute_metrics, city_scores
from visualization import build_horizon_chart, build_heatmap
from config import DATA_PROCESSED_DIR, OUTPUTS_DIR


def main() -> None:
    villes_df = build_cities_df()
    coords_df = build_coords_df(villes_df)
    df_forecasts = collect_forecasts(coords_df)
    df_historique = build_synthetic_history(villes_df, days=30, seed=42)
    df_metrics = compute_metrics(df_historique)
    df_scores = city_scores(df_metrics)

    villes_df.to_csv(DATA_PROCESSED_DIR / "villes.csv", index=False)
    coords_df.to_csv(DATA_PROCESSED_DIR / "coords.csv", index=False)
    df_forecasts.to_csv(DATA_PROCESSED_DIR / "forecasts.csv", index=False)
    df_historique.to_csv(DATA_PROCESSED_DIR / "historique.csv", index=False)
    df_metrics.to_csv(DATA_PROCESSED_DIR / "metrics.csv", index=False)
    df_scores.to_csv(DATA_PROCESSED_DIR / "city_scores.csv", index=False)

    fig1 = build_horizon_chart(df_metrics)
    fig2 = build_heatmap(df_metrics)
    fig1.write_html(OUTPUTS_DIR / "mae_horizon.html")
    fig2.write_html(OUTPUTS_DIR / "heatmap_scores.html")

    print("Exports termines")
    print("CSV :", DATA_PROCESSED_DIR)
    print("HTML:", OUTPUTS_DIR)


if __name__ == "__main__":
    main()
