-- Command:
-- python manage.py sqlcustom core | python manage.py dbshell
DELETE FROM core_chcategory;

-- Free time // Aficiones y ocio
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Free time - General', 'Free time', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Learn languages', 'Free time', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Cooking & Recipes', 'Free time', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Collecting', 'Free time', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Photography', 'Free time', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Board and role-playing games', 'Free time', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Humor', 'Free time', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Music production & Instruments', 'Free time', 'Dummy description');

-- Love & friendship // Amor y amistad
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Friendship', 'Love & Friendship', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Love', 'Love & Friendship', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Sexuality', 'Love & Friendship', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Relationship problems', 'Love & Friendship', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Weddings & Bachelor(ette) parties', 'Love & Friendship', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('LGBT', 'Love & Friendship', 'Dummy description');

-- Art & cultural events // Arte y eventos culturales
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Art & Cultural events', 'Art & Cultural events', 'Dummy description');

-- Natural sciences // Ciencias naturales
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Natural sciences - General', 'Natural sciences', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Astronomy', 'Natural sciences', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Biology', 'Natural sciences', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Physics', 'Natural sciences', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Chemistry', 'Natural sciences', 'Dummy description');

-- Social sciences // Ciencias sociales
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Social sciences', 'Social sciences', 'Dummy description');

-- Movies & TV // Cine y TV
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Movies & TV - General', 'Movies & TV', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Anime', 'Movies & TV', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Movies & TV - Celebrities', 'Movies & TV', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Movies', 'Movies & TV', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Series', 'Movies & TV', 'Dummy description');

-- Shopping & Market // Compras y mercadillo
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Shopping & Market', 'Shopping & Market', 'Dummy description');

-- Meet new people // Conocer gente
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Meet new people - General', 'Meet new people', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Activities', 'Meet new people', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Dating', 'Meet new people', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Events', 'Meet new people', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Musicians & Bands', 'Meet new people', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Meetups', 'Meet new people', 'Dummy description');

-- Sports // Deporte
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Sports - General', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Basketball', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Baseball', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Cricket', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Amateur sports and meetups', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Motorsports', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Football', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Golf', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Hockey', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Rugby & American football', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Tennis', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Table tennis', 'Sports', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Volleyball', 'Sports', 'Dummy description');

-- Education // Educación
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Education - General', 'Education', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Compulsory education', 'Education', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Postgraduate studies', 'Education', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Vocational training', 'Education', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Preschool', 'Education', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('University', 'Education', 'Dummy description');

-- Lifestyle // Estilo de vida
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Lifestyle - General', 'Lifestyle', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Beauty', 'Lifestyle', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Moods', 'Lifestyle', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Phylosophy & Spirituality', 'Lifestyle', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Fashion', 'Lifestyle', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Geek life', 'Lifestyle', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Nightlife', 'Lifestyle', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Subcultures', 'Lifestyle', 'Dummy description');

-- Family, Home & Pets // Familia, hogar y mascotas
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Decoration & Home care', 'Family, Home & Pets', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Family', 'Family, Home & Pets', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Gardening', 'Family, Home & Pets', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Maternity & Paternity', 'Family, Home & Pets', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Pets', 'Family, Home & Pets', 'Dummy description');

-- Internet // Internet
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Internet', 'Internet', 'Dummy description');

-- Books & Comics // Libros y cómics
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Books & Comics', 'Libros y cómics', 'Dummy description');

-- Cars, Motorbikes & Others // Motor
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Cars, Motorbikes & Others - General', 'Cars, Motorbikes & Others', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Cars', 'Cars, Motorbikes & Others', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Motorbikes', 'Cars, Motorbikes & Others', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Yachts', 'Cars, Motorbikes & Others', 'Dummy description');

-- Music // Música
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Music', 'Music', 'Dummy description');

-- News & Current affairs // Noticias y actualidad
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('News & Current affairs', 'News & Current affairs', 'Dummy description');

-- Politics & Activism // Política y activismo
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Politics & Activism', 'Politics & Activism', 'Dummy description');

-- Health & Fitness // Salud y fitness
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Health - General', 'Health & Fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Diets', 'Health & Fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Disabilities', 'Health & Fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Fitness', 'Health & Fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Alternative medicine', 'Health & Fitness', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Psychology & Psychiatry', 'Health & Fitness', 'Dummy description');

-- Places, Companies & Brands // Sitios, empresas y marcas
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Places, Companies & Brands', 'Places, Companies & Brands', 'Dummy description');

-- Technology & Computers // Tecnología e informática
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Technology & Computers - General', 'Technology & Computers', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Software & Operating systems', 'Technology & Computers', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Hardware', 'Technology & Computers', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Smartphones & Apps', 'Technology & Computers', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Software development', 'Technology & Computers', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Hacking', 'Technology & Computers', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Wearables', 'Technology & Computers', 'Dummy description');

-- Work & Business // Trabajo y negocios
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Work & Business - General', 'Work & Business', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Crowdfunding', 'Work & Business', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Entrepreneurs & Startups', 'Work & Business', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Finances', 'Work & Business', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Job vacancies', 'Work & Business', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Profession', 'Work & Business', 'Dummy description');

-- Trips & Places // Viajes y lugares
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Trips & Places - General', 'Trips & Places', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Trips - destination', 'Trips & Places', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Landmarks', 'Trips & Places', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Travel planning', 'Trips & Places', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Cultures & Ethnic groups', 'Trips & Places', 'Dummy description');

-- Video games // Videojuegos
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Video games - General', 'Video games', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Game consoles & Handheld', 'Video games', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Indie games', 'Video games', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('PC games', 'Video games', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "description")
  VALUES ('Smartphone games', 'Video games', 'Dummy description');
