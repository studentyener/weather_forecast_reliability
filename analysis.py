from __future__ import annotations

import numpy as np
import pandas as pd


def build_synthetic_history(villes_df: pd.DataFrame, days: int = 30, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days, freq="D")
    records = []
    for _, row in villes_df.iterrows():
        lat_effect = (float(row["lat"]) - 45.0) * -0.35
        city_bias = rng.normal(0, 0.8)
        for date in dates:
            seasonal = 6.0 * np.sin((date.dayofyear / 365.25) * 2 * np.pi)
            observed = 14 + lat_effect + seasonal + city_bias + rng.normal(0, 2.5)
            forecast = observed + rng.normal(0, 1.8) + city_bias * 0.15
            records.append(
                {
                    "date": date,
                    "ville": row["ville"],
                    "pays": row["pays"],
                    "observed_temp_c": round(float(observed), 2),
                    "forecast_temp_c": round(float(forecast), 2),
                }
            )
    return pd.DataFrame(records)


def compute_metrics(df_historique: pd.DataFrame) -> pd.DataFrame:
    df = df_historique.copy()
    df["error"] = df["forecast_temp_c"] - df["observed_temp_c"]
    grouped = (
        df.groupby(["ville", "pays"], as_index=False)
        .agg(
            mae=("error", lambda s: float(np.mean(np.abs(s)))),
            rmse=("error", lambda s: float(np.sqrt(np.mean(np.square(s))))),
            bias=("error", "mean"),
            observations=("error", "size"),
        )
    )
    grouped["reliability_index"] = 100 / (1 + grouped["mae"] + 0.5 * grouped["rmse"] + grouped["bias"].abs())
    return grouped.round({"mae": 2, "rmse": 2, "bias": 2, "reliability_index": 2})


def city_scores(df_metrics: pd.DataFrame) -> pd.DataFrame:
    df = df_metrics.copy()
    score = 100 - (df["mae"] * 18 + df["rmse"] * 10 + df["bias"].abs() * 8)
    df["score"] = score.clip(lower=0, upper=100).round(2)
    return df.sort_values(["score", "reliability_index"], ascending=[False, False]).reset_index(drop=True)
