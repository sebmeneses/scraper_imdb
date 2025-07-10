-- 1. Obtener las 5 décadas con mayor promedio de duración
SELECT
    (anio / 10) * 10 AS decada,
    AVG(duracion) AS promedio_duracion_decada
FROM peliculas
WHERE anio IS NOT NULL AND duracion IS NOT NULL
GROUP BY decada
ORDER BY promedio_duracion_decada DESC
LIMIT 5;

-- 2. Calcular la desviación estándar de las calificaciones por año
SELECT
    anio,
    STDDEV_POP(calificacion) AS desviacion_estandar_calificacion
FROM peliculas
WHERE calificacion IS NOT NULL AND anio IS NOT NULL
GROUP BY anio
ORDER BY anio;

-- 3. Detectar películas con más de un 20% de diferencia entre calificación IMDB y Metascore (normalizado)
SELECT
    titulo,
    anio,
    calificacion,
    metascore,
    ABS(calificacion * 10 - metascore) AS diferencia_absoluta,
    (ABS(calificacion * 10 - metascore) / metascore) * 100 AS porcentaje_diferencia
FROM peliculas
WHERE metascore IS NOT NULL AND calificacion IS NOT NULL
  AND (ABS(calificacion * 10 - metascore) / metascore) > 0.20
ORDER BY porcentaje_diferencia DESC;

-- 4. Crear una vista que relacione películas y actores, y permita filtrar por actor principal
CREATE OR REPLACE VIEW vista_peliculas_actores AS
SELECT
    p.id AS pelicula_id,
    p.titulo,
    p.anio,
    p.calificacion,
    p.duracion,
    p.metascore,
    a.nombre AS actor_principal
FROM peliculas p
JOIN actores a ON p.id = a.pelicula_id;

-- Para filtrar por actor principal:
-- SELECT * FROM vista_peliculas_actores WHERE actor_principal ILIKE '%NombreActor%';

-- 5. Crear un índice para optimizar búsquedas por actor principal
CREATE INDEX IF NOT EXISTS idx_actores_nombre ON actores(nombre);

-- Opcional: índice para búsquedas frecuentes por año y calificación en peliculas
CREATE INDEX IF NOT EXISTS idx_peliculas_anio_calificacion ON peliculas(anio, calificacion);
