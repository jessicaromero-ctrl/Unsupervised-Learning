# Historial de Cambios

Todos los cambios notables a este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y el proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [Sin publicar]

### Pendiente
- Manejo explícito del caso borde de división por cero en `pct_screen` (L-1)
- Validación de columnas esperadas al momento de carga (L-4)
- Parametrización del umbral `video_game_lover` vía argumento de línea de comandos
- Suite de pruebas de integración con datos sintéticos

---

## [0.2.0] — 2025

### Añadido
- Variable derivada `pct_screen`: proporción de entretenimiento en pantalla sobre total
- Variable derivada `video_game_lover`: indicador binario con umbral de 7 horas/semana
- Diagnóstico de valores faltantes antes y después de imputación (etapas 2 y 5)
- Estadísticas descriptivas en salida de consola (etapa 6)

### Cambiado
- La variable `video_game_lover` ahora se construye **después** de la imputación por media para evitar clasificación errónea de valores faltantes como `0`
- El pipeline ahora imprime el shape final con el comentario de target para facilitar validación visual

### Corregido
- Separador decimal inconsistente (coma/punto) en `hours_per_week` ahora normalizado antes del cast a `float64`

---

## [0.1.0] — 2025

### Añadido
- Carga de datos desde `entertainment.csv` en formato largo
- Pivot `long → wide` con `pivot_table` y `aggfunc="mean"`
- Selección de columnas en orden canónico: `name`, `video_games`, `tv_shows`, `movies`, `books`
- Exportación del DataFrame transformado a `entertainment_wide.csv`
