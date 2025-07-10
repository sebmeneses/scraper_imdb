CREATE TABLE peliculas (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    anio INT,
    calificacion NUMERIC(3,1),
    duracion INT,
    metascore INT,
    UNIQUE(titulo, anio)  -- Aquí agregas la restricción UNIQUE
);

CREATE TABLE actores (
    id SERIAL PRIMARY KEY,
    pelicula_id INT REFERENCES peliculas(id) ON DELETE CASCADE,
    nombre VARCHAR(255) NOT NULL
);
