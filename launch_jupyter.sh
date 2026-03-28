#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
jupyter notebook weather_forecast_final.ipynb
