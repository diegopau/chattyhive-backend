# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


# TODO: podría ser conveniente añadir una excepción en caso de que el grupo al que se intenta añadir no exista.
def add_category(CategoryModel, name, description, code, group):
    category = CategoryModel(name=name, description=description, code=code, group=group)
    category.save()


def create_categories(apps, schema_editor):
    CategoryModel = apps.get_model("core", "ChCategory")
    print("CategoryModel: ", CategoryModel)
    # Art & cultural events // Arte y eventos culturales
    add_category(CategoryModel, 'Art & Cultural events', 'Art & Cultural events', '01.01', 'Dummy description')

    # Books & Comics // Libros y cómics
    add_category(CategoryModel, 'Books & Comics', 'Books & Comics', '02.01', 'Dummy description')

    # Cars, Motorbikes & Others // Motor
    add_category(CategoryModel, 'Cars, Motorbikes & Others - General', 'Cars, Motorbikes & Others', '03.01', 'Dummy description')
    add_category(CategoryModel, 'Cars', 'Cars, Motorbikes & Others', '03.02', 'Dummy description')
    add_category(CategoryModel, 'Motorbikes', 'Cars, Motorbikes & Others', '03.03', 'Dummy description')
    add_category(CategoryModel, 'Yachts', 'Cars, Motorbikes & Others', '03.04', 'Dummy description')

    # Education // Educación
    add_category(CategoryModel, 'Education - General', 'Education', '04.01', 'Dummy description')
    add_category(CategoryModel, 'Compulsory education', 'Education', '04.02', 'Dummy description')
    add_category(CategoryModel, 'Postgraduate studies', 'Education', '04.03', 'Dummy description')
    add_category(CategoryModel, 'Preschool', 'Education', '04.04', 'Dummy description')
    add_category(CategoryModel, 'University', 'Education', '04.05', 'Dummy description')
    add_category(CategoryModel, 'Vocational training', 'Education', '04.06', 'Dummy description')

    # Family, Home & Pets // Familia, hogar y mascotas
    add_category(CategoryModel, 'Decoration & Home care', 'Family, Home & Pets', '05.01', 'Dummy description')
    add_category(CategoryModel, 'Family', 'Family, Home & Pets', '05.02', 'Dummy description')
    add_category(CategoryModel, 'Gardening', 'Family, Home & Pets', '05.03', 'Dummy description')
    add_category(CategoryModel, 'Maternity & Paternity', 'Family, Home & Pets', '05.04', 'Dummy description')
    add_category(CategoryModel, 'Pets', 'Family, Home & Pets', '05.05', 'Dummy description')

    # Free time // Aficiones y ocio
    add_category(CategoryModel, 'Free time - General', 'Free time', '06.01', 'Dummy description')
    add_category(CategoryModel, 'Board and role-playing games', 'Free time', '06.02', 'Dummy description')
    add_category(CategoryModel, 'Collecting', 'Free time', '06.03', 'Dummy description')
    add_category(CategoryModel, 'Cooking & Recipes', 'Free time', '06.04', 'Dummy description')
    add_category(CategoryModel, 'Humor', 'Free time', '06.05', 'Dummy description')
    add_category(CategoryModel, 'Learn languages', 'Free time', '06.06', 'Dummy description')
    add_category(CategoryModel, 'Music production & Instruments', 'Free time', '06.07', 'Dummy description')
    add_category(CategoryModel, 'Photography', 'Free time', '06.08', 'Dummy description')

    # Health & Fitness // Salud y fitness
    add_category(CategoryModel, 'Health - General', 'Health & Fitness', '07.01', 'Dummy description')
    add_category(CategoryModel, 'Alternative medicine', 'Health & Fitness', '07.02', 'Dummy description')
    add_category(CategoryModel, 'Diets', 'Health & Fitness', '07.03', 'Dummy description')
    add_category(CategoryModel, 'Disabilities', 'Health & Fitness', '07.04', 'Dummy description')
    add_category(CategoryModel, 'Fitness', 'Health & Fitness', '07.05', 'Dummy description')
    add_category(CategoryModel, 'Psychology & Psychiatry', 'Health & Fitness', '07.06', 'Dummy description')

    # Internet // Internet
    add_category(CategoryModel, 'Internet', 'Internet', '08.01', 'Dummy description')

    # Lifestyle // Estilo de vida
    add_category(CategoryModel, 'Lifestyle - General', 'Lifestyle', '09.01', 'Dummy description')
    add_category(CategoryModel, 'Beauty', 'Lifestyle', '09.02', 'Dummy description')
    add_category(CategoryModel, 'Fashion', 'Lifestyle', '09.03', 'Dummy description')
    add_category(CategoryModel, 'Geek life', 'Lifestyle', '09.04', 'Dummy description')
    add_category(CategoryModel, 'Moods', 'Lifestyle', '09.05', 'Dummy description')
    add_category(CategoryModel, 'Nightlife', 'Lifestyle', '09.06', 'Dummy description')
    add_category(CategoryModel, 'Phylosophy & Spirituality', 'Lifestyle', '09.07', 'Dummy description')
    add_category(CategoryModel, 'Subcultures', 'Lifestyle', '09.08', 'Dummy description')

    # Love & friendship // Amor y amistad
    add_category(CategoryModel, 'Friendship', 'Love & Friendship', '10.01', 'Dummy description')
    add_category(CategoryModel, 'LGBT', 'Love & Friendship', '10.02', 'Dummy description')
    add_category(CategoryModel, 'Love', 'Love & Friendship', '10.03', 'Dummy description')
    add_category(CategoryModel, 'Relationship problems', 'Love & Friendship', '10.04', 'Dummy description')
    add_category(CategoryModel, 'Sexuality', 'Love & Friendship', '10.05', 'Dummy description')
    add_category(CategoryModel, 'Weddings & Bachelor(ette) parties', 'Love & Friendship', '10.06', 'Dummy description')

    # Meet new people // Conocer gente
    add_category(CategoryModel, 'Meet new people - General', 'Meet new people', '11.01', 'Dummy description')
    add_category(CategoryModel, 'Activities', 'Meet new people', '11.02', 'Dummy description')
    add_category(CategoryModel, 'Dating', 'Meet new people', '11.03', 'Dummy description')
    add_category(CategoryModel, 'Events', 'Meet new people', '11.04', 'Dummy description')
    add_category(CategoryModel, 'Meetups', 'Meet new people', '11.05', 'Dummy description')
    add_category(CategoryModel, 'Musicians & Bands', 'Meet new people', '11.06', 'Dummy description')

    # Movies & TV // Cine y TV
    add_category(CategoryModel, 'Movies & TV - General', 'Movies & TV', '12.01', 'Dummy description')
    add_category(CategoryModel, 'Anime', 'Movies & TV', '12.02', 'Dummy description')
    add_category(CategoryModel, 'Movies', 'Movies & TV', '12.03', 'Dummy description')
    add_category(CategoryModel, 'Movies & TV - Celebrities', 'Movies & TV', '12.04', 'Dummy description')
    add_category(CategoryModel, 'Series', 'Movies & TV', '12.05', 'Dummy description')

    # Natural sciences // Ciencias naturales
    add_category(CategoryModel, 'Natural sciences - General', 'Natural sciences', '13.01', 'Dummy description')
    add_category(CategoryModel, 'Astronomy', 'Natural sciences', '13.02', 'Dummy description')
    add_category(CategoryModel, 'Biology', 'Natural sciences', '13.03', 'Dummy description')
    add_category(CategoryModel, 'Chemistry', 'Natural sciences', '13.04', 'Dummy description')
    add_category(CategoryModel, 'Physics', 'Natural sciences', '13.05', 'Dummy description')

    # Music // Música
    add_category(CategoryModel, 'Music', 'Music', '14.01', 'Dummy description')

    # News & Current affairs // Noticias y actualidad
    add_category(CategoryModel, 'News & Current affairs', 'News & Current affairs', '15.01', 'Dummy description')

    # Places, Companies & Brands // Sitios, empresas y marcas
    add_category(CategoryModel, 'Places, Companies & Brands', 'Places, Companies & Brands', '16.01', 'Dummy description')

    # Politics & Activism // Política y activismo
    add_category(CategoryModel, 'Politics & Activism', 'Politics & Activism', '17.01', 'Dummy description')

    # Shopping & Market // Compras y mercadillo
    add_category(CategoryModel, 'Shopping & Market', 'Shopping & Market', '18.01', 'Dummy description')

    # Social sciences // Ciencias sociales
    add_category(CategoryModel, 'Social sciences', 'Social sciences', '19.01', 'Dummy description')

    # Sports // Deporte
    add_category(CategoryModel, 'Sports - General', 'Sports', '20.01', 'Dummy description')
    add_category(CategoryModel, 'Amateur sports and meetups', 'Sports', '20.02', 'Dummy description')
    add_category(CategoryModel, 'Baseball', 'Sports', '20.03', 'Dummy description')
    add_category(CategoryModel, 'Basketball', 'Sports', '20.04', 'Dummy description')
    add_category(CategoryModel, 'Cricket', 'Sports', '20.05', 'Dummy description')
    add_category(CategoryModel, 'Football', 'Sports', '20.06', 'Dummy description')
    add_category(CategoryModel, 'Golf', 'Sports', '20.07', 'Dummy description')
    add_category(CategoryModel, 'Hockey', 'Sports', '20.08', 'Dummy description')
    add_category(CategoryModel, 'Motorsports', 'Sports', '20.09', 'Dummy description')
    add_category(CategoryModel, 'Rugby & American football', 'Sports', '20.10', 'Dummy description')
    add_category(CategoryModel, 'Table tennis', 'Sports', '20.11', 'Dummy description')
    add_category(CategoryModel, 'Tennis', 'Sports', '20.12', 'Dummy description')
    add_category(CategoryModel, 'Volleyball', 'Sports', '20.13', 'Dummy description')

    #Technology & Computers // Tecnología e informática
    add_category(CategoryModel, 'Technology & Computers - General', 'Technology & Computers', '21.01', 'Dummy description')
    add_category(CategoryModel, 'Hacking', 'Technology & Computers', '21.02', 'Dummy description')
    add_category(CategoryModel, 'Hardware', 'Technology & Computers', '21.03', 'Dummy description')
    add_category(CategoryModel, 'Smartphones & Apps', 'Technology & Computers', '21.04', 'Dummy description')
    add_category(CategoryModel, 'Software & Operating systems', 'Technology & Computers', '21.05', 'Dummy description')
    add_category(CategoryModel, 'Software development', 'Technology & Computers', '21.06', 'Dummy description')
    add_category(CategoryModel, 'Wearables', 'Technology & Computers', '21.07', 'Dummy description')

    # Trips & Places // Viajes y lugares
    add_category(CategoryModel, 'Trips & Places - General', 'Trips & Places', '22.01', 'Dummy description')
    add_category(CategoryModel, 'Cultures & Ethnic groups', 'Trips & Places', '22.02', 'Dummy description')
    add_category(CategoryModel, 'Landmarks', 'Trips & Places', '22.03', 'Dummy description')
    add_category(CategoryModel, 'Travel planning', 'Trips & Places', '22.04', 'Dummy description')
    add_category(CategoryModel, 'Trips - destination', 'Trips & Places', '22.05', 'Dummy description')

    # Video games // Videojuegos
    add_category(CategoryModel, 'Video games - General', 'Video games', '23.01', 'Dummy description')
    add_category(CategoryModel, 'Game consoles & Handheld', 'Video games', '23.02', 'Dummy description')
    add_category(CategoryModel, 'Indie games', 'Video games', '23.03', 'Dummy description')
    add_category(CategoryModel, 'PC games', 'Video games', '23.04', 'Dummy description')
    add_category(CategoryModel, 'Smartphone games', 'Video games', '23.05', 'Dummy description')

    # Work & Business // Trabajo y negocios
    add_category(CategoryModel, 'Work & Business - General', 'Work & Business', '24.01', 'Dummy description')
    add_category(CategoryModel, 'Crowdfunding', 'Work & Business', '24.02', 'Dummy description')
    add_category(CategoryModel, 'Entrepreneurs & Startups', 'Work & Business', '24.03', 'Dummy description')
    add_category(CategoryModel, 'Finances', 'Work & Business', '24.04', 'Dummy description')
    add_category(CategoryModel, 'Job vacancies', 'Work & Business', '24.05', 'Dummy description')
    add_category(CategoryModel, 'Profession', 'Work & Business', '24.06', 'Dummy description')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
