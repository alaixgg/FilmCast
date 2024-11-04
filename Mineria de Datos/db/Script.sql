-- Eliminar las tablas si ya existen en el orden correcto para evitar errores de dependencias
DROP TABLE IF EXISTS actividad;
DROP TABLE IF EXISTS proyectos;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS actores;

-- Crear la tabla usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    clave VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    descripcion TEXT,
    Pais VARCHAR(50)
);

-- Crear la tabla proyectos
CREATE TABLE proyectos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    genero VARCHAR(20) CHECK (genero IN ('Comedy', 'Action', 'Horror', 'Musical', 'Drama', 'Sci-Fi')),
    fecha_inicio DATE,
    fecha_fin DATE,
    presupuesto DECIMAL(15, 2)
);

-- Crear la tabla actividad, vinculada a usuarios y proyectos
CREATE TABLE actividad (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    proyecto_id INTEGER REFERENCES proyectos(id) ON DELETE SET NULL,
    actor_id INTEGER REFERENCES Actores(id) ON DELETE CASCADE,  -- Agregar relación con actores
    rol VARCHAR(50),  -- rol que el usuario tuvo en el proyecto
    fecha_inicio DATE,
    fecha_fin DATE
);

-- Crear la tabla actores
CREATE TABLE actores (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(6) CHECK (gender IN ('Female', 'Male')),
    nationality VARCHAR(50) CHECK (nationality IN ('USA', 'Canada')),
    years_active INTEGER,
    genre_specialization VARCHAR(20) CHECK (genre_specialization IN ('Comedy', 'Action', 'Horror', 'Musical', 'Drama', 'Sci-Fi')),
    beauty FLOAT CHECK (beauty BETWEEN 1 AND 17),
    skill_level FLOAT CHECK (skill_level BETWEEN 1 AND 17),
    education_level VARCHAR(20) CHECK (education_level IN ('Graduate', 'High School', 'College', 'University')),
    award_wins INTEGER,
    media_mentions INTEGER,
    social_media_followers INTEGER,
    social_media_likes INTEGER,
    network_size INTEGER,
    income DECIMAL(15, 2)
);

-- Insertar datos en la tabla usuarios
INSERT INTO usuarios (nombre, clave, telefono, email, descripcion, Pais) VALUES
('a', 'a', '3045418711', 'a@gmail.com', 'Director conocido por su enfoque técnico y narrativo complejo en películas de alto presupuesto y profundas temáticas psicológicas.', 'USA'),
('daniela', 'daniela', '3002654412', 'daniela@gmail.com', 'Directora icónica del cine independiente estadounidense, famosa por su uso estilizado de la violencia y diálogos elaborados.', 'USA'),
('alaix', 'alaix', '3181028389', 'alaixjp@gmail.com', 'Director reconocido por su exploración de las emociones humanas y su uso de personajes femeninos fuertes en el cine canadiense.', 'Canada'),
('julian', 'julian', '384570399', 'julian@gmail.com', 'Director surcoreano conocido por su habilidad para mezclar géneros y por sus críticas sociales a través de historias intrigantes y visualmente ricas.', 'USA'),
('t', 't', '3003948856', 't@gmail.com', 'hola?', 'Canada'),
('h', 'h', '304456000000', 'h@gmail.com', NULL, 'Canada');

-- Insertar registros en la tabla Actores
INSERT INTO Actores (name, age, gender, nationality, years_active, genre_specialization, beauty, skill_level, education_level, award_wins, media_mentions, social_media_followers, social_media_likes, network_size, income) VALUES
('Anthony Vaughn', 19, 'Female', 'USA', 1, 'Comedy', 10, 8, 'University', 7, 52, 15678, 4914, 22, 434056.09),
('Justin Osborn', 48, 'Male', 'USA', 19, 'Drama', 8, 10, 'College', 10, 37, 18420, 5378, 30, 1188216.47),
('Sandra Kim', 49, 'Male', 'USA', 23, 'Sci-Fi', 7, 10, 'College', 12, 46, 17382, 5033, 23, 1730313.22),
('Mark Hahn', 41, 'Female', 'USA', 15, 'Sci-Fi', 8, 10, 'Graduate', 9, 42, 16742, 5005, 25, 818967.94),
('Julie Brown', 38, 'Male', 'USA', 19, 'Action', 6, 10, 'University', 11, 38, 13428, 4662, 22, 974068.97),
('Jonathan Robinson', 31, 'Female', 'USA', 13, 'Action', 6, 10, 'Graduate', 9, 45, 19001, 5572, 27, 1112517.18),
('William Flynn', 46, 'Male', 'USA', 9, 'Sci-Fi', 6, 7, 'College', 7, 37, 15585, 5488, 27, 475294.21),
('Jamie Smith', 23, 'Female', 'Canada', 5, 'Drama', 5, 8, 'College', 6, 34, 14159, 4998, 23, 229526.53),
('Michael Reyes', 20, 'Female', 'USA', 2, 'Action', 8, 8, 'Graduate', 6, 39, 16617, 5715, 28, 486564.72),
('Ann Webb', 42, 'Male', 'USA', 13, 'Sci-Fi', 8, 3, 'College', 8, 26, 16297, 5207, 24, 757637.41),
('Megan Wilson', 25, 'Female', 'Canada', 7, 'Action', 5, 5, 'Graduate', 5, 48, 17038, 5205, 26, 498028.17),
('Chad Murphy', 28, 'Female', 'USA', 10, 'Drama', 9, 8, 'College', 10, 44, 17324, 4883, 25, 912692.75), 
('Brian Kemp', 37, 'Female', 'USA', 16, 'Drama', 9, 6, 'University', 9, 39, 14220, 4877, 27, 841281.56),
('Sara Walter', 49, 'Female', 'USA', 15, 'Comedy', 8, 6, 'University', 7, 27, 15655, 5278, 24, 555912.45);

-- Insertar registros en la tabla proyectos
INSERT INTO proyectos (titulo, descripcion, genero, fecha_inicio, fecha_fin, presupuesto) VALUES
('Caminos Inexplorados', 'Una historia sobre la búsqueda de identidad en un mundo cambiante.', 'Drama', '2023-01-15', '2023-06-30', 2500000.00),
('El Último Susurro', 'Un thriller psicológico que examina los límites de la moralidad.', 'Horror', '2022-03-01', '2022-12-15', 1800000.00),
('Danza de Estrellas', 'Un musical que narra la vida de una joven bailarina en Broadway.', 'Musical', '2023-07-10', '2023-12-20', 1500000.00),
('Aventuras Espaciales', 'Un grupo de astronautas exploran un planeta desconocido.', 'Sci-Fi', '2024-02-01', '2024-11-30', 3000000.00),
('Risas en el Tiempo', 'Una comedia que muestra los altibajos de una familia a través de las décadas.', 'Comedy', '2024-05-15', '2025-01-01', 1200000.00);
-- Insertar registros en la tabla actividad
-- Insertar registros en la tabla actividad
INSERT INTO actividad (usuario_id, proyecto_id, actor_id, rol, fecha_inicio, fecha_fin) VALUES
(1, 1, 1, 'Actor Principal', '2023-01-15', '2023-06-30'),  -- Anthony Vaughn
(2, 2, 2, 'Actor Secundario', '2022-03-01', '2022-12-15'),  -- Justin Osborn
(3, 3, 3, 'Actor Principal', '2023-07-10', '2023-12-20'),  -- Sandra Kim
(1, 4, 4, 'Actor de Reparto', '2024-02-01', '2024-11-30'),  -- Mark Hahn
(2, 5, 5, 'Actor Principal', '2024-05-15', '2025-01-01');    -- Julie Brown


