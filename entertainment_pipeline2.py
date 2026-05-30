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
print(f"[2] Nulos detectados tras cast:\n{df.isna().sum()}\n")

# Determinar granularidad: 1 fila por estudiante 
print(f"[3] Estudiantes únicos: {df['name'].nunique()}")
print(f"    Categorías únicas:  {df['entertainment'].unique()}\n")

# Crear una columna total_entertainment para cada estudiante
total_entertainment = df.groupby("name")["hours_per_week"].sum()

# Pivot long → wide 
df_wide = df.pivot_table(
    index="name",
    columns="entertainment",
    values="hours_per_week",
    aggfunc="mean",
).reset_index()
df_wide.columns.name = None
df_wide = df_wide[["name", "video_games", "tv_shows", "movies", "books"]]
print(f"[4] Shape tras pivot (wide): {df_wide.shape}")

# Encontrar los valores faltantes en cada columna
missing_values = df_wide.isna().sum()
print("\nValores faltantes por columna:")
print(missing_values)

# Rellenar los valores faltantes con 0's
df_wide_filled = df_wide.fillna(0)
print("\nValores faltantes después de rellenar con 0's:")

# Imputar nulos con media de columna
print(f"\n[5] Nulos por columna antes de imputación:\n{df_wide.isna().sum()}")
for col in ["video_games", "tv_shows", "movies", "books"]:
    col_mean = round(df_wide[col].mean(), 2)
    df_wide[col] = df_wide[col].fillna(col_mean)
print(f"\n    Nulos tras imputación:\n{df_wide.isna().sum()}\n")

# Crear video_game_lover DESPUÉS de imputar, sobre df_wide
df_wide["video_game_lover"] = (df_wide["video_games"] > 7).astype(int)

# Crear una columna llamada pct_screen que calcule el porcentaje de entretenimiento que se consume
# pantallas (todo, excepto libros) para cada estudiante
df_wide["pct_screen"] = (
    (df_wide["video_games"] + df_wide["tv_shows"] + df_wide["movies"])
    / (df_wide["video_games"] + df_wide["tv_shows"] + df_wide["movies"] + df_wide["books"])
).round(3)

# Verificar y guardar
print(f"[6] Shape final: {df_wide.shape}  ← target: (150, 5)")
print(df_wide.head(5), "\n")
print("[6] Estadísticas descriptivas:")
print(df_wide.describe().round(3))

df_wide.to_csv("entertainment_wide.csv", index=False)
print("\n✓ Guardado: entertainment_wide.csv")