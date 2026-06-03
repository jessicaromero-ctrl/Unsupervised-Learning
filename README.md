# Pipeline de Transformación de Datos de Entretenimiento

> Pipeline ETL para reestructuración, imputación y enriquecimiento de datos de consumo de entretenimiento estudiantil. Transforma formato largo (*long*) a formato ancho (*wide*) con ingeniería de características derivadas.

---

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Lógica del Pipeline](#lógica-del-pipeline)
- [Características Generadas](#características-generadas)
- [Decisiones de Diseño](#decisiones-de-diseño)
- [Limitaciones Conocidas](#limitaciones-conocidas)
- [Licencia](#licencia)

---

## Descripción General

Este proyecto implementa un pipeline de procesamiento de datos en Python/pandas para transformar un conjunto de datos de consumo de entretenimiento estudiantil desde su formato original (largo, una fila por categoría por estudiante) hacia un formato analítico estructurado (ancho, una fila por estudiante). El pipeline cubre limpieza de tipos, detección de valores faltantes, imputación por media de columna, y construcción de dos variables derivadas: un indicador binario de videojugadores frecuentes (`video_game_lover`) y una proporción de consumo en pantalla (`pct_screen`).

**Fuente de datos esperada:** `entertainment.csv` — archivo CSV con columnas `name`, `entertainment`, `hours_per_week`.

**Salida producida:** `entertainment_wide.csv` — una fila por estudiante, cuatro columnas de categorías, más las dos variables derivadas.

---

## Estructura del Repositorio

```
entertainment-pipeline/
├── entertainment_pipeline2.py   # Script principal del pipeline ETL
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Documentación principal
├── CHANGELOG.md                 # Historial de cambios
├── .gitignore                   # Exclusiones de control de versiones
├── data/
│   └── README.md                # Descripción del esquema de datos esperado
├── docs/
│   └── decisiones_diseno.md     # Registro de decisiones de arquitectura (ADR)
└── tests/
    └── test_pipeline.py         # Pruebas unitarias del pipeline
```

---

## Requisitos

| Dependencia | Versión mínima | Propósito                          |
|-------------|----------------|------------------------------------|
| Python      | 3.9+           | Entorno de ejecución               |
| pandas      | 1.5.0+         | Manipulación de datos tabulares    |
| numpy       | 1.23.0+        | Operaciones numéricas de soporte   |

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/<usuario>/entertainment-pipeline.git
cd entertainment-pipeline

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows (PowerShell)

# Instalar dependencias
pip install -r requirements.txt
```

---

## Uso

1. Colocar el archivo `entertainment.csv` en el directorio raíz del proyecto (ver `data/README.md` para el esquema esperado).
2. Ejecutar el pipeline:

```bash
python entertainment_pipeline2.py
```

3. El archivo de salida `entertainment_wide.csv` se generará en el directorio raíz.

**Salida esperada en consola (resumen):**

```
[1] Shape original (long): (N, 3)
[2] Nulos detectados tras cast: ...
[3] Estudiantes únicos: 150  Categorías únicas: ['video_games', 'tv_shows', 'movies', 'books']
[4] Shape tras pivot (wide): (150, 5)
[5] Nulos por columna antes de imputación: ...
[6] Shape final: (150, 7)  ← target: (150, 5)
✓ Guardado: entertainment_wide.csv
```

> **Nota:** El mensaje `← target: (150, 5)` en el log `[6]` refleja el número de columnas del pivot original; el DataFrame final contiene 7 columnas dado que se añaden `video_game_lover` y `pct_screen`.

---

## Lógica del Pipeline

El pipeline ejecuta seis etapas secuenciales:

| Etapa | Operación                                                                                       |
|-------|-------------------------------------------------------------------------------------------------|
| 1     | Carga del CSV en formato largo                                                                  |
| 2     | Normalización del separador decimal (coma → punto) y conversión a `float64`                    |
| 3     | Diagnóstico de granularidad (estudiantes únicos, categorías presentes)                          |
| 4     | Pivot de formato largo a ancho (`pivot_table` con `aggfunc="mean"`)                             |
| 5     | Detección e imputación de valores faltantes (media de columna, por categoría)                   |
| 6     | Ingeniería de características: `video_game_lover`, `pct_screen`; exportación a CSV             |

---

## Características Generadas

### `video_game_lover` (binaria)

Indicador que toma el valor `1` si el estudiante reporta más de 7 horas semanales en videojuegos, y `0` en caso contrario. El umbral de 7 horas fue establecido como parámetro exploratorio inicial y puede ajustarse según el análisis downstream.

```python
df_wide["video_game_lover"] = (df_wide["video_games"] > 7).astype(int)
```

### `pct_screen` (razón continua ∈ [0, 1])

Proporción del total de horas de entretenimiento consumida en medios de pantalla (videojuegos, series de televisión, películas), excluyendo libros.

```
pct_screen = (video_games + tv_shows + movies) / (video_games + tv_shows + movies + books)
```

**Advertencia:** Si un estudiante tiene cero horas en todas las categorías, esta operación produce `NaN` por división entre cero. El pipeline no maneja actualmente este caso borde (ver [Limitaciones Conocidas](#limitaciones-conocidas)).

---

## Decisiones de Diseño

Ver `docs/decisiones_diseno.md` para el registro completo de decisiones de arquitectura. Las principales son:

- **Imputación por media:** Se seleccionó la media de columna como estrategia de imputación por ser conservadora y reproducible en contexto exploratorio. No se aplicó imputación por mediana ni métodos multivariados (KNN, MICE) dado el alcance del proyecto.
- **`aggfunc="mean"` en pivot:** En caso de duplicados (mismo estudiante, misma categoría, múltiples registros), se promedia en lugar de sumar para mantener la unidad de medida (horas/semana).
- **Orden de operaciones:** La variable `video_game_lover` se construye *después* de la imputación para evitar clasificar como `0` a estudiantes que tenían `NaN` por dato faltante y no por ausencia real de consumo.

---

## Limitaciones Conocidas

| ID  | Descripción                                                                                  | Severidad |
|-----|----------------------------------------------------------------------------------------------|-----------|
| L-1 | División por cero en `pct_screen` si todas las horas son `0` tras imputación                | Media     |
| L-2 | El umbral `> 7` en `video_game_lover` no tiene validación empírica; es un parámetro fijo    | Baja      |
| L-3 | El log `[6]` reporta `target: (150, 5)` pero el shape real es `(150, 7)` — inconsistencia  | Baja      |
| L-4 | No se valida que las cuatro categorías esperadas estén presentes en el CSV de entrada       | Media     |

---

## Licencia

Distribuido bajo licencia MIT. Ver `LICENSE` para más detalles.
