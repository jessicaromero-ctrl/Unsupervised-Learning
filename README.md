# Datos

Este directorio está reservado para archivos de datos locales. **Los datos no se versionan** (ver `.gitignore`).

---

## Esquema de entrada: `entertainment.csv`

El pipeline espera un archivo CSV en formato **largo** (*long format*) con la siguiente estructura:

| Columna          | Tipo esperado | Descripción                                                                 |
|------------------|---------------|-----------------------------------------------------------------------------|
| `name`           | `str`         | Identificador del estudiante (nombre o clave única)                         |
| `entertainment`  | `str`         | Categoría de entretenimiento. Valores válidos: `video_games`, `tv_shows`, `movies`, `books` |
| `hours_per_week` | `float`       | Horas semanales dedicadas a la categoría. Acepta coma o punto como separador decimal |

### Ejemplo de estructura esperada

```
name,entertainment,hours_per_week
Estudiante_001,video_games,3.5
Estudiante_001,tv_shows,7,0
Estudiante_001,movies,2.0
Estudiante_001,books,1.5
Estudiante_002,video_games,10.0
...
```

### Restricciones

- Se espera exactamente **150 estudiantes únicos** en la configuración de referencia.
- Cada estudiante puede tener entre 1 y 4 filas (una por categoría). Las categorías ausentes se imputarán con la media de columna.
- Los valores de `hours_per_week` deben ser no negativos. Valores negativos no son filtrados por el pipeline actual.

---

## Esquema de salida: `entertainment_wide.csv`

| Columna            | Tipo     | Descripción                                                           |
|--------------------|----------|-----------------------------------------------------------------------|
| `name`             | `str`    | Identificador del estudiante                                          |
| `video_games`      | `float`  | Horas/semana en videojuegos (imputada si faltante)                    |
| `tv_shows`         | `float`  | Horas/semana en series de televisión (imputada si faltante)           |
| `movies`           | `float`  | Horas/semana en películas (imputada si faltante)                      |
| `books`            | `float`  | Horas/semana en lectura (imputada si faltante)                        |
| `video_game_lover` | `int`    | `1` si `video_games > 7`, `0` en caso contrario                      |
| `pct_screen`       | `float`  | Proporción de horas en pantalla sobre total. Rango esperado: [0, 1]  |
