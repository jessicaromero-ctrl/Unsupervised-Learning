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

# Encontrar valores faltantes
print("\nValores faltantes por columna:")
print(df_wide.isna().sum())

# Rellenar valores faltantes con ceros
df_wide = df_wide.fillna(0)
print("\nValores faltantes después de rellenar con 0's:")
print(df_wide.isna().sum())

# video_game_lover: 1 si juega más de 7 hrs/semana
df_wide["video_game_lover"] = (df_wide["video_games"] > 7).astype(int)

print(f"\nShape final: {df_wide.shape}")
print(df_wide.head(5))
print(df_wide.describe().round(3))

df_wide.to_csv("entertainment_wide_img2.csv", index=False)
print("\n✓ Guardado: entertainment_wide_img2.csv")