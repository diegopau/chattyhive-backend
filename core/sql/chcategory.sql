
-- Command:
-- python manage.py sqlcustom core | python manage.py dbshell
DELETE FROM core_chcategory;

-- Aficiones y ocio
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Aficiones y ocio - general', 'Aficiones y ocio', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Aprender idiomas', 'Aficiones y ocio', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Cocina y recetas', 'Aficiones y ocio', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Coleccionismo', 'Aficiones y ocio', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Fotografía', 'Aficiones y ocio', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Juegos de rol y de mesa', 'Aficiones y ocio', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Humor', 'Aficiones y ocio', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Producción musical e instrumentos', 'Aficiones y ocio', 'Dummy description');

-- Amor y amistad
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Amistad', 'Amor y amistad', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Amor', 'Amor y amistad', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Sexualidad', 'Amor y amistad', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Problemas de pareja', 'Amor y amistad', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Bodas y despedidas de solter@', 'Amor y amistad', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('LGBT', 'Amor y amistad', 'Dummy description');

-- Arte y eventos culturales
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Arte y eventos culturales', 'Arte y eventos culturales', 'Dummy description');

-- Ciencias naturales
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Ciencia', 'Ciencias naturales', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Astronomía', 'Ciencias naturales', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Biología', 'Ciencias naturales', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Física', 'Ciencias naturales', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Química', 'Ciencias naturales', 'Dummy description');

-- Ciencias sociales
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Ciencias sociales', 'Ciencias sociales', 'Dummy description');

-- Cine y TV
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Cine y TV - varios', 'Cine y TV', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Anime', 'Cine y TV', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Cine y TV - Famosos', 'Cine y TV', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Películas', 'Cine y TV', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Series', 'Cine y TV', 'Dummy description');

-- Compras y mercadillo
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Compras y mercadillo', 'Compras y mercadillo', 'Dummy description');

-- Conocer gente
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Conocer gente - general', 'Conocer gente', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Actividades', 'Conocer gente', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Buscar pareja', 'Conocer gente', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Eventos', 'Conocer gente', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Músicos y bandas', 'Conocer gente', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Quedadas', 'Conocer gente', 'Dummy description');

-- Deporte
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Deportes - otros', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Baloncesto', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Béisbol', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Cricket', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Deporte amateur y quedadas', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Deportes de motor', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Fútbol', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Golf', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Hockey', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Rugby y fútbol americano', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Tenis', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Tenis de mesa', 'Deporte', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Voleibol', 'Deporte', 'Dummy description');

-- Educación
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Educación - Otros', 'Educación', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Educación obligatoria', 'Educación', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Estudios de postgrado', 'Educación', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Formación profesional', 'Educación', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Preescolar', 'Educación', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Universidad', 'Educación', 'Dummy description');

-- Estilo de vida
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Estilo de vida - general', 'Estilo de vida', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Belleza', 'Estilo de vida', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Estados de ánimo', 'Estilo de vida', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Filosofía y espiritualidad', 'Estilo de vida', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Moda', 'Estilo de vida', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Vida nocturna', 'Estilo de vida', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Subculturas', 'Estilo de vida', 'Dummy description');

-- Familia y hogar
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Decoración / cuidados del hogar', 'Familia y hogar', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Familia', 'Familia y hogar', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Jardinería', 'Familia y hogar', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Maternidad / paternidad', 'Familia y hogar', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Mascotas', 'Familia y hogar', 'Dummy description');

-- Internet
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Internet', 'Internet', 'Dummy description');

-- Libros y cómics
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Libros y cómics', 'Libros y cómics', 'Dummy description');

-- Motor
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Motor - varios', 'Motor', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Coches', 'Motor', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Motos', 'Motor', 'Dummy description');

-- Música
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Música', 'Música', 'Dummy description');

-- Noticias y actualidad
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Noticias y actualidad', 'Noticias y actualidad', 'Dummy description');

-- Política y activismo
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Política y activismo', 'Política y activismo', 'Dummy description');

-- Salud y fitness
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Salud - general', 'Salud y fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Dietas y nutrición', 'Salud y fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Discapacidades', 'Salud y fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Fitness', 'Salud y fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Medicina alternativa', 'Salud y fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Psicología y psiquiatría', 'Salud y fitness', 'Dummy description');

-- Sitios, empresas y marcas
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Sitios, empresas y marcas', 'Sitios, empresas y marcas', 'Dummy description');

-- Tecnología e informática
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Tecnología e informática - general', 'Tecnología e informática', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Software y sistemas operativos', 'Tecnología e informática', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Hardware', 'Tecnología e informática', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Smartphones y apps', 'Tecnología e informática', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Desarrollo de software', 'Tecnología e informática', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Hacking', 'Tecnología e informática', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Wearables', 'Tecnología e informática', 'Dummy description');

-- Trabajo y negocios
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Crowdfunding', 'Trabajo y negocios', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Emprendedores y startups', 'Trabajo y negocios', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Finanzas', 'Trabajo y negocios', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Oferta y demanda de trabajo', 'Trabajo y negocios', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Profesiones', 'Trabajo y negocios', 'Dummy description');

-- Viajes y turismo
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Viajes - destinos', 'Viajes y turismo', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Puntos de interés', 'Viajes y turismo', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Organizar viajes', 'Viajes y turismo', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Culturas y etnias', 'Viajes y turismo', 'Dummy description');

-- Videojuegos
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Videojuegos - otros', 'Videojuegos', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Consola y portátiles', 'Videojuegos', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Indie', 'Videojuegos', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('PC', 'Videojuegos', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Smartphones', 'Videojuegos', 'Dummy description');