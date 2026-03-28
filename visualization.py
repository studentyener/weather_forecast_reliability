import pandas as pd
import plotly.express as px


def build_horizon_chart(df_metrics: pd.DataFrame):
    fig = px.bar(
        df_metrics.sort_values("mae"),
        x="ville",
        y="mae",
        color="pays",
        title="Erreur absolue moyenne par ville",
        labels={"ville": "Ville", "mae": "MAE (°C)", "pays": "Pays"},
    )
    fig.update_layout(xaxis_title="Ville", yaxis_title="MAE (°C)")
    return fig


def build_heatmap(df_metrics: pd.DataFrame):
    matrix = (
        df_metrics.set_index("ville")[["mae", "rmse", "bias", "reliability_index"]]
        .sort_index()
    )
    fig = px.imshow(
        matrix,
        text_auto=".2f",
        aspect="auto",
        title="Comparaison des indicateurs de fiabilité",
        labels={"x": "Indicateur", "y": "Ville", "color": "Valeur"},
    )
    return fig
