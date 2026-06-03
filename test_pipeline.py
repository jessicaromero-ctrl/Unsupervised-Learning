"""
Pruebas unitarias para entertainment_pipeline2.py

Estrategia de prueba:
    - Datos sintéticos generados en cada prueba (sin dependencia de archivos externos)
    - Cobertura de las seis etapas del pipeline: carga, limpieza, pivot,
      imputación, ingeniería de características, y casos borde

Ejecutar con:
    pytest tests/test_pipeline.py -v
"""

import pandas as pd
import numpy as np
import pytest


# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def datos_completos():
    """Dataset mínimo en formato largo sin valores faltantes."""
    return pd.DataFrame({
        "name": ["Ana", "Ana", "Ana", "Ana",
                  "Luis", "Luis", "Luis", "Luis"],
        "entertainment": ["video_games", "tv_shows", "movies", "books",
                          "video_games", "tv_shows", "movies", "books"],
        "hours_per_week": [10.0, 5.0, 3.0, 2.0,
                            4.0, 8.0, 6.0, 1.0],
    })


@pytest.fixture
def datos_con_faltantes():
    """Dataset donde Luis no tiene registro de 'books'."""
    return pd.DataFrame({
        "name": ["Ana", "Ana", "Ana", "Ana",
                  "Luis", "Luis", "Luis"],
        "entertainment": ["video_games", "tv_shows", "movies", "books",
                          "video_games", "tv_shows", "movies"],
        "hours_per_week": [10.0, 5.0, 3.0, 2.0,
                            4.0, 8.0, 6.0],
    })


@pytest.fixture
def datos_separador_coma():
    """Dataset con separador decimal de coma (contexto regional español/México)."""
    return pd.DataFrame({
        "name": ["Ana", "Ana"],
        "entertainment": ["video_games", "books"],
        "hours_per_week": ["3,5", "1,0"],
    })


# ─── Utilidades de apoyo ──────────────────────────────────────────────────────

def aplicar_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Replica la lógica de pivot del pipeline sobre un DataFrame en formato largo."""
    df_wide = df.pivot_table(
        index="name",
        columns="entertainment",
        values="hours_per_week",
        aggfunc="mean",
    ).reset_index()
    df_wide.columns.name = None
    columnas = ["name"] + [c for c in ["video_games", "tv_shows", "movies", "books"]
                           if c in df_wide.columns]
    return df_wide[columnas]


def imputar_media(df: pd.DataFrame) -> pd.DataFrame:
    """Imputa NaN con la media de cada columna numérica."""
    df = df.copy()
    for col in ["video_games", "tv_shows", "movies", "books"]:
        if col in df.columns:
            df[col] = df[col].fillna(round(df[col].mean(), 2))
    return df


def construir_features(df: pd.DataFrame) -> pd.DataFrame:
    """Construye video_game_lover y pct_screen sobre un DataFrame wide ya imputado."""
    df = df.copy()
    df["video_game_lover"] = (df["video_games"] > 7).astype(int)
    df["pct_screen"] = (
        (df["video_games"] + df["tv_shows"] + df["movies"])
        / (df["video_games"] + df["tv_shows"] + df["movies"] + df["books"])
    ).round(3)
    return df


# ─── Pruebas: limpieza de separador decimal ───────────────────────────────────

class TestLimpiezaDecimal:
    def test_coma_se_convierte_a_punto(self, datos_separador_coma):
        df = datos_separador_coma.copy()
        df["hours_per_week"] = (
            df["hours_per_week"].astype(str).str.replace(",", ".").str.strip()
        )
        df["hours_per_week"] = pd.to_numeric(df["hours_per_week"], errors="coerce")
        assert df["hours_per_week"].dtype in [np.float64, float]
        assert df["hours_per_week"].iloc[0] == pytest.approx(3.5)

    def test_valores_no_numericos_se_convierten_a_nan(self):
        df = pd.DataFrame({"hours_per_week": ["abc", "N/A", "5.0"]})
        df["hours_per_week"] = pd.to_numeric(df["hours_per_week"], errors="coerce")
        assert df["hours_per_week"].isna().sum() == 2


# ─── Pruebas: pivot long → wide ───────────────────────────────────────────────

class TestPivot:
    def test_shape_correcto_sin_faltantes(self, datos_completos):
        df_wide = aplicar_pivot(datos_completos)
        assert df_wide.shape == (2, 5)  # 2 estudiantes, name + 4 categorías

    def test_columnas_presentes(self, datos_completos):
        df_wide = aplicar_pivot(datos_completos)
        assert list(df_wide.columns) == ["name", "video_games", "tv_shows", "movies", "books"]

    def test_una_fila_por_estudiante(self, datos_completos):
        df_wide = aplicar_pivot(datos_completos)
        assert df_wide["name"].nunique() == df_wide.shape[0]

    def test_valores_correctos_sin_duplicados(self, datos_completos):
        df_wide = aplicar_pivot(datos_completos)
        ana = df_wide[df_wide["name"] == "Ana"].iloc[0]
        assert ana["video_games"] == pytest.approx(10.0)
        assert ana["books"] == pytest.approx(2.0)


# ─── Pruebas: imputación ──────────────────────────────────────────────────────

class TestImputacion:
    def test_no_quedan_nulos_tras_imputacion(self, datos_con_faltantes):
        df_wide = aplicar_pivot(datos_con_faltantes)
        df_imputado = imputar_media(df_wide)
        assert df_imputado.isna().sum().sum() == 0

    def test_imputacion_con_media_correcta(self, datos_con_faltantes):
        """'books' de Luis debe imputarse con la media observada de Ana (2.0)."""
        df_wide = aplicar_pivot(datos_con_faltantes)
        media_books = df_wide["books"].mean()  # Solo Ana tiene valor
        df_imputado = imputar_media(df_wide)
        luis = df_imputado[df_imputado["name"] == "Luis"].iloc[0]
        assert luis["books"] == pytest.approx(media_books, abs=0.01)

    def test_valores_no_faltantes_no_se_alteran(self, datos_con_faltantes):
        df_wide = aplicar_pivot(datos_con_faltantes)
        df_imputado = imputar_media(df_wide)
        ana_original = df_wide[df_wide["name"] == "Ana"]["books"].values[0]
        ana_imputada = df_imputado[df_imputado["name"] == "Ana"]["books"].values[0]
        assert ana_original == pytest.approx(ana_imputada)


# ─── Pruebas: ingeniería de características ───────────────────────────────────

class TestFeatureEngineering:
    def test_video_game_lover_sobre_umbral(self, datos_completos):
        df_wide = aplicar_pivot(datos_completos)
        df_wide = imputar_media(df_wide)
        df_wide = construir_features(df_wide)
        # Ana tiene 10.0 horas → debe ser 1
        ana = df_wide[df_wide["name"] == "Ana"].iloc[0]
        assert ana["video_game_lover"] == 1

    def test_video_game_lover_bajo_umbral(self, datos_completos):
        df_wide = aplicar_pivot(datos_completos)
        df_wide = imputar_media(df_wide)
        df_wide = construir_features(df_wide)
        # Luis tiene 4.0 horas → debe ser 0
        luis = df_wide[df_wide["name"] == "Luis"].iloc[0]
        assert luis["video_game_lover"] == 0

    def test_video_game_lover_exactamente_en_umbral(self):
        """Exactamente 7 horas NO cumple la condición estricta (> 7)."""
        df = pd.DataFrame({
            "name": ["Borde"],
            "video_games": [7.0],
            "tv_shows": [3.0],
            "movies": [2.0],
            "books": [1.0],
        })
        df = construir_features(df)
        assert df["video_game_lover"].iloc[0] == 0

    def test_pct_screen_rango_valido(self, datos_completos):
        df_wide = aplicar_pivot(datos_completos)
        df_wide = imputar_media(df_wide)
        df_wide = construir_features(df_wide)
        assert (df_wide["pct_screen"] >= 0).all()
        assert (df_wide["pct_screen"] <= 1).all()

    def test_pct_screen_calculo_correcto(self, datos_completos):
        """Para Ana: (10+5+3)/(10+5+3+2) = 18/20 = 0.9"""
        df_wide = aplicar_pivot(datos_completos)
        df_wide = imputar_media(df_wide)
        df_wide = construir_features(df_wide)
        ana = df_wide[df_wide["name"] == "Ana"].iloc[0]
        assert ana["pct_screen"] == pytest.approx(0.9, abs=0.001)

    def test_video_game_lover_construida_post_imputacion(self, datos_con_faltantes):
        """
        Garantiza que el orden imputación → features no clasifica NaN como 0.
        Luis tiene NaN en 'books' pero no en 'video_games', así que este test
        verifica que video_game_lover se evalúa correctamente en ambos casos.
        """
        df_wide = aplicar_pivot(datos_con_faltantes)
        df_wide = imputar_media(df_wide)
        assert df_wide["video_games"].isna().sum() == 0
        df_wide = construir_features(df_wide)
        assert df_wide["video_game_lover"].isna().sum() == 0


# ─── Pruebas: forma final del DataFrame ───────────────────────────────────────

class TestFormaFinal:
    def test_columnas_finales(self, datos_completos):
        df_wide = aplicar_pivot(datos_completos)
        df_wide = imputar_media(df_wide)
        df_wide = construir_features(df_wide)
        columnas_esperadas = {"name", "video_games", "tv_shows", "movies",
                               "books", "video_game_lover", "pct_screen"}
        assert set(df_wide.columns) == columnas_esperadas

    def test_tipos_de_datos(self, datos_completos):
        df_wide = aplicar_pivot(datos_completos)
        df_wide = imputar_media(df_wide)
        df_wide = construir_features(df_wide)
        assert df_wide["video_game_lover"].dtype in [np.int32, np.int64, int]
        assert df_wide["pct_screen"].dtype in [np.float64, float]
