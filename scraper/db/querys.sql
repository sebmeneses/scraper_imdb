
--- 5 décadas con mayor promedio de duración
SELECT
    (anio / 10) * 10 AS decada,
    AVG(duracion) AS promedio_duracion_decada
FROM peliculas
WHERE anio IS NOT NULL AND duracion IS NOT NULL
GROUP BY decada
ORDER BY promedio_duracion_decada DESC
LIMIT 5;

-- Desviación estándar por año
SELECT
    anio,
    STDDEV_POP(calificacion) AS desviacion_estandar_calificacion
FROM peliculas
WHERE calificacion IS NOT NULL AND anio IS NOT NULL
GROUP BY anio
ORDER BY anio;

-- Películas con diferencia > 20% entre IMDB y Metascore

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


--Vista para películas y actores (filtrable)
CREATE OR REPLACE VIEW vista_peliculas_actores AS
SELECT
    p.id AS pelicula_id,
    p.titulo,
    p.anio,
    p.calificacion,
    p.d


-- busqueda actor y peliculas. 
SELECT * FROM vista_peliculas_actores WHERE actor_principal ILIKE '%Morgan Freeman%';

-- Crear un índice para optimizar búsquedas por actor principal
CREATE INDEX IF NOT EXISTS idx_actores_nombre ON actores(nombre);

-- índice para búsquedas frecuentes por año y calificación en peliculas
CREATE INDEX IF NOT EXISTS idx_peliculas_anio_calificacion ON peliculas(anio, calificacion);