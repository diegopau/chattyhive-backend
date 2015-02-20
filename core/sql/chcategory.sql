-- Command:
-- python manage.py sqlcustom core | python manage.py dbshell
DELETE FROM core_chcategory;

-- Art & cultural events // Arte y eventos culturales
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Art & Cultural events', 'Art & Cultural events', '01.01', 'Dummy description');

-- Books & Comics // Libros y cómics
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Books & Comics', 'Books & Comics', '02.01', 'Dummy description');


-- Cars, Motorbikes & Others // Motor
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Cars, Motorbikes & Others - General', 'Cars, Motorbikes & Others', '03.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Cars', 'Cars, Motorbikes & Others', '03.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Motorbikes', 'Cars, Motorbikes & Others', '03.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Yachts', 'Cars, Motorbikes & Others', '03.04', 'Dummy description');



-- Education // Educación
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Education - General', 'Education', '04.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Compulsory education', 'Education', '04.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Postgraduate studies', 'Education', '04.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Preschool', 'Education', '04.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('University', 'Education', '04.05', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Vocational training', 'Education', '04.06', 'Dummy description');


-- Family, Home & Pets // Familia, hogar y mascotas
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Decoration & Home care', 'Family, Home & Pets', '05.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Family', 'Family, Home & Pets', '05.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Gardening', 'Family, Home & Pets', '05.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Maternity & Paternity', 'Family, Home & Pets', '05.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Pets', 'Family, Home & Pets', '05.05', 'Dummy description');


-- Free time // Aficiones y ocio
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Free time - General', 'Free time', '06.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Board and role-playing games', 'Free time', '06.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Collecting', 'Free time', '06.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Cooking & Recipes', 'Free time', '06.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Humor', 'Free time', '06.05', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Learn languages', 'Free time', '06.06', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Music production & Instruments', 'Free time', '06.07', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Photography', 'Free time', '06.08', 'Dummy description');

-- Health & Fitness // Salud y fitness
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Health - General', 'Health & Fitness', '07.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Alternative medicine', 'Health & Fitness', '07.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Diets', 'Health & Fitness', '07.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Disabilities', 'Health & Fitness', '07.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Fitness', 'Health & Fitness', '07.05', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Psychology & Psychiatry', 'Health & Fitness', '07.06', 'Dummy description');

-- Internet // Internet
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Internet', 'Internet', '08.01', 'Dummy description');

-- Lifestyle // Estilo de vida
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Lifestyle - General', 'Lifestyle', '09.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Beauty', 'Lifestyle', '09.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Fashion', 'Lifestyle', '09.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Geek life', 'Lifestyle', '09.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Moods', 'Lifestyle', '09.05', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Nightlife', 'Lifestyle', '09.06', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Phylosophy & Spirituality', 'Lifestyle', '09.07', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Subcultures', 'Lifestyle', '09.08', 'Dummy description');

-- Love & friendship // Amor y amistad
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Friendship', 'Love & Friendship', '10.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('LGBT', 'Love & Friendship', '10.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Love', 'Love & Friendship', '10.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Relationship problems', 'Love & Friendship', '10.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Sexuality', 'Love & Friendship', '10.05', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Weddings & Bachelor(ette) parties', 'Love & Friendship', '10.06', 'Dummy description');

-- Meet new people // Conocer gente
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Meet new people - General', 'Meet new people', '11.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Activities', 'Meet new people', '11.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Dating', 'Meet new people', '11.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Events', 'Meet new people', '11.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Meetups', 'Meet new people', '11.05', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Musicians & Bands', 'Meet new people', '11.06', 'Dummy description');

-- Movies & TV // Cine y TV
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Movies & TV - General', 'Movies & TV', '12.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Anime', 'Movies & TV', '12.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Movies', 'Movies & TV', '12.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Movies & TV - Celebrities', 'Movies & TV', '12.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Series', 'Movies & TV', '12.05', 'Dummy description');

-- Natural sciences // Ciencias naturales
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Natural sciences - General', 'Natural sciences', '13.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Astronomy', 'Natural sciences', '13.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Biology', 'Natural sciences', '13.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Chemistry', 'Natural sciences', '13.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Physics', 'Natural sciences', '13.05', 'Dummy description');

-- Music // Música
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Music', 'Music', '14.01', 'Dummy description');

-- News & Current affairs // Noticias y actualidad
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('News & Current affairs', 'News & Current affairs', '15.01', 'Dummy description');

-- Places, Companies & Brands // Sitios, empresas y marcas
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Places, Companies & Brands', 'Places, Companies & Brands', '16.01', 'Dummy description');

-- Politics & Activism // Política y activismo
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Politics & Activism', 'Politics & Activism', '17.01', 'Dummy description');

-- Shopping & Market // Compras y mercadillo
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Shopping & Market', 'Shopping & Market', '18.01', 'Dummy description');

-- Social sciences // Ciencias sociales
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Social sciences', 'Social sciences', '19.01', 'Dummy description');

-- Sports // Deporte
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Sports - General', 'Sports', '20.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Amateur sports and meetups', 'Sports', '20.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Baseball', 'Sports', '20.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Basketball', 'Sports', '20.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Cricket', 'Sports', '20.05', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Football', 'Sports', '20.06', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Golf', 'Sports', '20.07', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Hockey', 'Sports', '20.08', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Motorsports', 'Sports', '20.09', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Rugby & American football', 'Sports', '20.10', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Table tennis', 'Sports', '20.11', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Tennis', 'Sports', '20.12', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Volleyball', 'Sports', '20.13', 'Dummy description');

-- Technology & Computers // Tecnología e informática
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Technology & Computers - General', 'Technology & Computers', '21.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Hacking', 'Technology & Computers', '21.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Hardware', 'Technology & Computers', '21.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Smartphones & Apps', 'Technology & Computers', '21.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Software & Operating systems', 'Technology & Computers', '21.05', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Software development', 'Technology & Computers', '21.06', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Wearables', 'Technology & Computers', '21.07', 'Dummy description');

-- Trips & Places // Viajes y lugares
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Trips & Places - General', 'Trips & Places', '22.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Cultures & Ethnic groups', 'Trips & Places', '22.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Landmarks', 'Trips & Places', '22.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Travel planning', 'Trips & Places', '22.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Trips - destination', 'Trips & Places', '22.05', 'Dummy description');

-- Video games // Videojuegos
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Video games - General', 'Video games', '23.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Game consoles & Handheld', 'Video games', '23.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Indie games', 'Video games', '23.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('PC games', 'Video games', '23.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Smartphone games', 'Video games', '23.05', 'Dummy description');

-- Work & Business // Trabajo y negocios
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Work & Business - General', 'Work & Business', '24.01', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Crowdfunding', 'Work & Business', '24.02', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Entrepreneurs & Startups', 'Work & Business', '24.03', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Finances', 'Work & Business', '24.04', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Job vacancies', 'Work & Business', '24.05', 'Dummy description');
INSERT INTO core_chcategory ("name", "group", "code", "description")
  VALUES ('Profession', 'Work & Business', '24.06', 'Dummy description');