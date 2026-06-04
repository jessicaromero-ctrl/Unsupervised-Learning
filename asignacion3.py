import pandas as pd
import numpy as np

# Importar datos
df = pd.read_csv("entertainment.csv")
print(f"[1] Shape original (long): {df.shape}")
print(df.head(4), "\n")

# Limpiar separador decimal
df["hours_per_week"] = (
    df["hours_per_week"].astype(str).str.replace(",", ".").str.strip()
)
df["hours_per_week"] = pd.to_numeric(df["hours_per_week"], errors="coerce")

# Pivot long → wide
df_wide = df.pivot_table(
    index="name",
    columns="entertainment",
    values="hours_per_week",
    aggfunc="mean",
).reset_index()
df_wide.columns.name = None
df_wide = df_wide[["name", "video_games", "tv_shows", "movies", "books"]]

# Imputar nulos con media de columna
for col in ["video_games", "tv_shows", "movies", "books"]:
    df_wide[col] = df_wide[col].fillna(round(df_wide[col].mean(), 2))

# total_entertainment: suma de todos los tipos por estudiante
df_wide["total_entertainment"] = (
    df_wide["video_games"] + df_wide["tv_shows"] + df_wide["movies"] + df_wide["books"]
)

# pct_screen: porcentaje de pantallas (todo excepto libros)
df_wide["pct_screen"] = (
    (df_wide["video_games"] + df_wide["tv_shows"] + df_wide["movies"])
    / df_wide["total_entertainment"]
).round(3)

print(f"Shape final: {df_wide.shape}")
print(df_wide.head(5))
print(df_wide.describe().round(3))

df_wide.to_csv("entertainment_wide_img1.csv", index=False)
print("\n✓ Guardado: entertainment_wide_img1.csv")