import os
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

try:
    import requests
except Exception:  # pragma: no cover
    requests = None


def build_cities_df() -> pd.DataFrame:
    """Create a small study panel of cities with coordinates."""
    cities = [
        {"ville": "Paris", "pays": "France", "lat": 48.8566, "lon": 2.3522},
        {"ville": "Lyon", "pays": "France", "lat": 45.7640, "lon": 4.8357},
        {"ville": "Marseille", "pays": "France", "lat": 43.2965, "lon": 5.3698},
        {"ville": "Strasbourg", "pays": "France", "lat": 48.5734, "lon": 7.7521},
        {"ville": "Lille", "pays": "France", "lat": 50.6292, "lon": 3.0573},
        {"ville": "Toulouse", "pays": "France", "lat": 43.6047, "lon": 1.4442},
        {"ville": "Nantes", "pays": "France", "lat": 47.2184, "lon": -1.5536},
        {"ville": "Nice", "pays": "France", "lat": 43.7102, "lon": 7.2620},
    ]
    return pd.DataFrame(cities)


def build_coords_df(villes_df: pd.DataFrame) -> pd.DataFrame:
    expected = ["ville", "pays", "lat", "lon"]
    return villes_df[expected].copy()


def _synthetic_forecasts(coords_df: pd.DataFrame, horizon_hours: int = 24) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    base_time = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    records = []
    for _, row in coords_df.iterrows():
        lat_effect = (float(row["lat"]) - 45.0) * -0.25
        for step in range(1, horizon_hours + 1):
            target_time = base_time + timedelta(hours=step)
            daily_wave = 7.0 * np.sin((target_time.hour / 24.0) * 2 * np.pi)
            temp = 15 + lat_effect + daily_wave + rng.normal(0, 1.3)
            humidity = int(np.clip(65 + rng.normal(0, 12), 25, 95))
            wind_speed = float(np.clip(12 + rng.normal(0, 4), 1, 40))
            records.append(
                {
                    "ville": row["ville"],
                    "pays": row["pays"],
                    "lat": row["lat"],
                    "lon": row["lon"],
                    "timestamp_utc": target_time.isoformat(),
                    "horizon_h": step,
                    "temperature_c": round(float(temp), 2),
                    "humidity_pct": humidity,
                    "wind_kmh": round(wind_speed, 2),
                    "source": "synthetic",
                }
            )
    return pd.DataFrame(records)


def _openweather_forecasts(coords_df: pd.DataFrame, api_key: str) -> pd.DataFrame:
    if requests is None:
        raise RuntimeError("Le package requests est indisponible dans cet environnement.")
    records = []
    for _, row in coords_df.iterrows():
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={
                "lat": row["lat"],
                "lon": row["lon"],
                "appid": api_key,
                "units": "metric",
                "lang": "fr",
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        for item in payload.get("list", []):
            wind = item.get("wind", {})
            main = item.get("main", {})
            records.append(
                {
                    "ville": row["ville"],
                    "pays": row["pays"],
                    "lat": row["lat"],
                    "lon": row["lon"],
                    "timestamp_utc": item.get("dt_txt"),
                    "horizon_h": None,
                    "temperature_c": main.get("temp"),
                    "humidity_pct": main.get("humidity"),
                    "wind_kmh": round(float(wind.get("speed", 0)) * 3.6, 2),
                    "source": "openweather",
                }
            )
    return pd.DataFrame(records)


def collect_forecasts(coords_df: pd.DataFrame) -> pd.DataFrame:
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if api_key:
        try:
            df = _openweather_forecasts(coords_df, api_key)
            if not df.empty:
                return df
        except Exception:
            pass
    return _synthetic_forecasts(coords_df)
