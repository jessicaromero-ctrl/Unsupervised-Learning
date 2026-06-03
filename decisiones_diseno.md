# Registro de Decisiones de Diseño

Este documento sigue el formato de *Architecture Decision Records* (ADR) propuesto por Michael Nygard. Cada decisión incluye contexto, opción elegida, alternativas consideradas y consecuencias.

---

## ADR-001: Estrategia de imputación de valores faltantes

**Estado:** Aceptada  
**Fecha:** 2025

### Contexto

El pivot de formato largo a ancho puede generar celdas vacías (`NaN`) cuando un estudiante no tiene registro para una o más categorías de entretenimiento. Se requiere una estrategia de imputación para garantizar que el DataFrame de salida esté completamente poblado.

### Decisión

Se imputa con la **media aritmética de cada columna** calculada sobre los datos observados (no imputados).

### Alternativas consideradas

| Alternativa          | Razón de descarte                                                              |
|----------------------|--------------------------------------------------------------------------------|
| Imputación con `0`   | Distorsionaría las medias y las proporciones derivadas (`pct_screen`)         |
| Mediana de columna   | Equivalente en muchos casos; la media es más interpretable para horas/semana  |
| KNN Imputer          | Complejidad computacional y de dependencias no justificada para el alcance     |
| MICE / IterativeImputer | Idem; reservada para análisis inferencial posterior                        |
| Eliminar filas       | Pérdida innecesaria de observaciones; el dataset es pequeño (≤150 estudiantes)|

### Consecuencias

- **Positivas:** Implementación simple, reproducible, sin dependencias adicionales.
- **Negativas:** La media puede introducir sesgo si los valores faltantes no son *Missing Completely at Random* (MCAR). No se realizó diagnóstico MCAR/MAR/MNAR.

---

## ADR-002: Función de agregación en `pivot_table`

**Estado:** Aceptada  
**Fecha:** 2025

### Contexto

`pandas.pivot_table` requiere especificar una función de agregación (`aggfunc`) para el caso en que existan filas duplicadas (mismo estudiante, misma categoría).

### Decisión

Se utiliza `aggfunc="mean"` para promediar los registros duplicados, preservando la unidad de medida original (horas/semana).

### Consecuencias

- Si existen duplicados legítimos (e.g., dos registros de `video_games` para el mismo estudiante en semanas distintas), se perderá información de varianza temporal.
- Se recomienda validar upstream que el CSV no contenga duplicados involuntarios antes de ejecutar el pipeline.

---

## ADR-003: Orden de construcción de variables derivadas

**Estado:** Aceptada  
**Fecha:** 2025

### Contexto

`video_game_lover` es una variable binaria que depende del valor de `video_games`. Si se construye antes de la imputación, los `NaN` se evaluarán como `False` (i.e., `NaN > 7 → False`), clasificando incorrectamente como no-jugadores a estudiantes con dato faltante.

### Decisión

`video_game_lover` se construye **siempre después** de la imputación por media.

### Consecuencias

- Un estudiante con `video_games = NaN` que sea imputado con la media de columna recibirá el valor de `video_game_lover` correspondiente a esa media, no necesariamente `0`. Esto es más conservador y analíticamente correcto que la asignación automática a `0`.

---

## ADR-004: Manejo del separador decimal

**Estado:** Aceptada  
**Fecha:** 2025

### Contexto

El CSV de entrada puede provenir de entornos con configuración regional en español (México/España), donde la coma (`,`) se usa como separador decimal. pandas no detecta esto automáticamente cuando el separador de columnas también es coma.

### Decisión

Se aplica `.str.replace(",", ".")` sobre la columna `hours_per_week` antes del cast a `float64`, seguido de `pd.to_numeric(..., errors="coerce")` para gestionar valores no convertibles sin lanzar excepción.

### Consecuencias

- Valores completamente no numéricos (e.g., `"N/A"`, cadenas de texto) se convertirán a `NaN` y serán imputados posteriormente.
- No se distingue entre coma-como-decimal y coma-como-separador-de-miles. Si el dataset contiene valores como `"1,500"` (mil quinientas horas), se interpretará como `1.500` (una hora y media). Documentar restricción en `data/README.md`.
