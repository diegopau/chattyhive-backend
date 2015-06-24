# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from slugify import Slugify

my_slugify = Slugify()
my_slugify.separator = '-'
my_slugify.pretranslate = {'&': 'and'}
my_slugify.to_lower = True
my_slugify.max_length = None
my_slugify.capitalize = False
my_slugify.safe_chars = ''


def add_slug(CategoryModel, category_name, category_group, category_code, category_description):
    category = CategoryModel.objects.get(code=category_code)
    category.slug = my_slugify(category_name)
    category.save()


def create_category_slugs(apps, schema_editor):
    CategoryModel = apps.get_model("core", "ChCategory")
    print("CategoryModel: ", CategoryModel)

    # Art & cultural events // Arte y eventos culturales
    add_slug(CategoryModel, 'Art & Cultural events', 'Art & Cultural events', '01.01', 'Dummy description')

    # Books & Comics // Libros y cómics
    add_slug(CategoryModel, 'Books & Comics', 'Books & Comics', '02.01', 'Dummy description')

    # Cars, Motorbikes & Others // Motor
    add_slug(CategoryModel, 'Cars, Motorbikes & Others - General', 'Cars, Motorbikes & Others', '03.01', 'Dummy description')
    add_slug(CategoryModel, 'Cars', 'Cars, Motorbikes & Others', '03.02', 'Dummy description')
    add_slug(CategoryModel, 'Motorbikes', 'Cars, Motorbikes & Others', '03.03', 'Dummy description')
    add_slug(CategoryModel, 'Yachts', 'Cars, Motorbikes & Others', '03.04', 'Dummy description')

    # Education // Educación
    add_slug(CategoryModel, 'Education - General', 'Education', '04.01', 'Dummy description')
    add_slug(CategoryModel, 'Compulsory education', 'Education', '04.02', 'Dummy description')
    add_slug(CategoryModel, 'Postgraduate studies', 'Education', '04.03', 'Dummy description')
    add_slug(CategoryModel, 'Preschool', 'Education', '04.04', 'Dummy description')
    add_slug(CategoryModel, 'University', 'Education', '04.05', 'Dummy description')
    add_slug(CategoryModel, 'Vocational training', 'Education', '04.06', 'Dummy description')

    # Family, Home & Pets // Familia, hogar y mascotas
    add_slug(CategoryModel, 'Decoration & Home care', 'Family, Home & Pets', '05.01', 'Dummy description')
    add_slug(CategoryModel, 'Family', 'Family, Home & Pets', '05.02', 'Dummy description')
    add_slug(CategoryModel, 'Gardening', 'Family, Home & Pets', '05.03', 'Dummy description')
    add_slug(CategoryModel, 'Maternity & Paternity', 'Family, Home & Pets', '05.04', 'Dummy description')
    add_slug(CategoryModel, 'Pets', 'Family, Home & Pets', '05.05', 'Dummy description')

    # Free time // Aficiones y ocio
    add_slug(CategoryModel, 'Free time - General', 'Free time', '06.01', 'Dummy description')
    add_slug(CategoryModel, 'Board and role-playing games', 'Free time', '06.02', 'Dummy description')
    add_slug(CategoryModel, 'Collecting', 'Free time', '06.03', 'Dummy description')
    add_slug(CategoryModel, 'Cooking & Recipes', 'Free time', '06.04', 'Dummy description')
    add_slug(CategoryModel, 'Humor', 'Free time', '06.05', 'Dummy description')
    add_slug(CategoryModel, 'Learn languages', 'Free time', '06.06', 'Dummy description')
    add_slug(CategoryModel, 'Music production & Instruments', 'Free time', '06.07', 'Dummy description')
    add_slug(CategoryModel, 'Photography', 'Free time', '06.08', 'Dummy description')

    # Health & Fitness // Salud y fitness
    add_slug(CategoryModel, 'Health - General', 'Health & Fitness', '07.01', 'Dummy description')
    add_slug(CategoryModel, 'Alternative medicine', 'Health & Fitness', '07.02', 'Dummy description')
    add_slug(CategoryModel, 'Diets', 'Health & Fitness', '07.03', 'Dummy description')
    add_slug(CategoryModel, 'Disabilities', 'Health & Fitness', '07.04', 'Dummy description')
    add_slug(CategoryModel, 'Fitness', 'Health & Fitness', '07.05', 'Dummy description')
    add_slug(CategoryModel, 'Psychology & Psychiatry', 'Health & Fitness', '07.06', 'Dummy description')

    # Internet // Internet
    add_slug(CategoryModel, 'Internet', 'Internet', '08.01', 'Dummy description')

    # Lifestyle // Estilo de vida
    add_slug(CategoryModel, 'Lifestyle - General', 'Lifestyle', '09.01', 'Dummy description')
    add_slug(CategoryModel, 'Beauty', 'Lifestyle', '09.02', 'Dummy description')
    add_slug(CategoryModel, 'Fashion', 'Lifestyle', '09.03', 'Dummy description')
    add_slug(CategoryModel, 'Geek life', 'Lifestyle', '09.04', 'Dummy description')
    add_slug(CategoryModel, 'Moods', 'Lifestyle', '09.05', 'Dummy description')
    add_slug(CategoryModel, 'Nightlife', 'Lifestyle', '09.06', 'Dummy description')
    add_slug(CategoryModel, 'Phylosophy & Spirituality', 'Lifestyle', '09.07', 'Dummy description')
    add_slug(CategoryModel, 'Subcultures', 'Lifestyle', '09.08', 'Dummy description')

    # Love & friendship // Amor y amistad
    add_slug(CategoryModel, 'Friendship', 'Love & Friendship', '10.01', 'Dummy description')
    add_slug(CategoryModel, 'LGBT', 'Love & Friendship', '10.02', 'Dummy description')
    add_slug(CategoryModel, 'Love', 'Love & Friendship', '10.03', 'Dummy description')
    add_slug(CategoryModel, 'Relationship problems', 'Love & Friendship', '10.04', 'Dummy description')
    add_slug(CategoryModel, 'Sexuality', 'Love & Friendship', '10.05', 'Dummy description')
    add_slug(CategoryModel, 'Weddings & Bachelor(ette) parties', 'Love & Friendship', '10.06', 'Dummy description')

    # Meet new people // Conocer gente
    add_slug(CategoryModel, 'Meet new people - General', 'Meet new people', '11.01', 'Dummy description')
    add_slug(CategoryModel, 'Activities', 'Meet new people', '11.02', 'Dummy description')
    add_slug(CategoryModel, 'Dating', 'Meet new people', '11.03', 'Dummy description')
    add_slug(CategoryModel, 'Events', 'Meet new people', '11.04', 'Dummy description')
    add_slug(CategoryModel, 'Meetups', 'Meet new people', '11.05', 'Dummy description')
    add_slug(CategoryModel, 'Musicians & Bands', 'Meet new people', '11.06', 'Dummy description')

    # Movies & TV // Cine y TV
    add_slug(CategoryModel, 'Movies & TV - General', 'Movies & TV', '12.01', 'Dummy description')
    add_slug(CategoryModel, 'Anime', 'Movies & TV', '12.02', 'Dummy description')
    add_slug(CategoryModel, 'Movies', 'Movies & TV', '12.03', 'Dummy description')
    add_slug(CategoryModel, 'Movies & TV - Celebrities', 'Movies & TV', '12.04', 'Dummy description')
    add_slug(CategoryModel, 'Series', 'Movies & TV', '12.05', 'Dummy description')

    # Natural sciences // Ciencias naturales
    add_slug(CategoryModel, 'Natural sciences - General', 'Natural sciences', '13.01', 'Dummy description')
    add_slug(CategoryModel, 'Astronomy', 'Natural sciences', '13.02', 'Dummy description')
    add_slug(CategoryModel, 'Biology', 'Natural sciences', '13.03', 'Dummy description')
    add_slug(CategoryModel, 'Chemistry', 'Natural sciences', '13.04', 'Dummy description')
    add_slug(CategoryModel, 'Physics', 'Natural sciences', '13.05', 'Dummy description')

    # Music // Música
    add_slug(CategoryModel, 'Music', 'Music', '14.01', 'Dummy description')

    # News & Current affairs // Noticias y actualidad
    add_slug(CategoryModel, 'News & Current affairs', 'News & Current affairs', '15.01', 'Dummy description')

    # Places, Companies & Brands // Sitios, empresas y marcas
    add_slug(CategoryModel, 'Places, Companies & Brands', 'Places, Companies & Brands', '16.01', 'Dummy description')

    # Politics & Activism // Política y activismo
    add_slug(CategoryModel, 'Politics & Activism', 'Politics & Activism', '17.01', 'Dummy description')

    # Shopping & Market // Compras y mercadillo
    add_slug(CategoryModel, 'Shopping & Market', 'Shopping & Market', '18.01', 'Dummy description')

    # Social sciences // Ciencias sociales
    add_slug(CategoryModel, 'Social sciences', 'Social sciences', '19.01', 'Dummy description')

    # Sports // Deporte
    add_slug(CategoryModel, 'Sports - General', 'Sports', '20.01', 'Dummy description')
    add_slug(CategoryModel, 'Amateur sports and meetups', 'Sports', '20.02', 'Dummy description')
    add_slug(CategoryModel, 'Baseball', 'Sports', '20.03', 'Dummy description')
    add_slug(CategoryModel, 'Basketball', 'Sports', '20.04', 'Dummy description')
    add_slug(CategoryModel, 'Cricket', 'Sports', '20.05', 'Dummy description')
    add_slug(CategoryModel, 'Football', 'Sports', '20.06', 'Dummy description')
    add_slug(CategoryModel, 'Golf', 'Sports', '20.07', 'Dummy description')
    add_slug(CategoryModel, 'Hockey', 'Sports', '20.08', 'Dummy description')
    add_slug(CategoryModel, 'Motorsports', 'Sports', '20.09', 'Dummy description')
    add_slug(CategoryModel, 'Rugby & American football', 'Sports', '20.10', 'Dummy description')
    add_slug(CategoryModel, 'Table tennis', 'Sports', '20.11', 'Dummy description')
    add_slug(CategoryModel, 'Tennis', 'Sports', '20.12', 'Dummy description')
    add_slug(CategoryModel, 'Volleyball', 'Sports', '20.13', 'Dummy description')

    #Technology & Computers // Tecnología e informática
    add_slug(CategoryModel, 'Technology & Computers - General', 'Technology & Computers', '21.01', 'Dummy description')
    add_slug(CategoryModel, 'Hacking', 'Technology & Computers', '21.02', 'Dummy description')
    add_slug(CategoryModel, 'Hardware', 'Technology & Computers', '21.03', 'Dummy description')
    add_slug(CategoryModel, 'Smartphones & Apps', 'Technology & Computers', '21.04', 'Dummy description')
    add_slug(CategoryModel, 'Software & Operating systems', 'Technology & Computers', '21.05', 'Dummy description')
    add_slug(CategoryModel, 'Software development', 'Technology & Computers', '21.06', 'Dummy description')
    add_slug(CategoryModel, 'Wearables', 'Technology & Computers', '21.07', 'Dummy description')

    # Trips & Places // Viajes y lugares
    add_slug(CategoryModel, 'Trips & Places - General', 'Trips & Places', '22.01', 'Dummy description')
    add_slug(CategoryModel, 'Cultures & Ethnic groups', 'Trips & Places', '22.02', 'Dummy description')
    add_slug(CategoryModel, 'Landmarks', 'Trips & Places', '22.03', 'Dummy description')
    add_slug(CategoryModel, 'Travel planning', 'Trips & Places', '22.04', 'Dummy description')
    add_slug(CategoryModel, 'Trips - destination', 'Trips & Places', '22.05', 'Dummy description')

    # Video games // Videojuegos
    add_slug(CategoryModel, 'Video games - General', 'Video games', '23.01', 'Dummy description')
    add_slug(CategoryModel, 'Game consoles & Handheld', 'Video games', '23.02', 'Dummy description')
    add_slug(CategoryModel, 'Indie games', 'Video games', '23.03', 'Dummy description')
    add_slug(CategoryModel, 'PC games', 'Video games', '23.04', 'Dummy description')
    add_slug(CategoryModel, 'Smartphone games', 'Video games', '23.05', 'Dummy description')

    # Work & Business // Trabajo y negocios
    add_slug(CategoryModel, 'Work & Business - General', 'Work & Business', '24.01', 'Dummy description')
    add_slug(CategoryModel, 'Crowdfunding', 'Work & Business', '24.02', 'Dummy description')
    add_slug(CategoryModel, 'Entrepreneurs & Startups', 'Work & Business', '24.03', 'Dummy description')
    add_slug(CategoryModel, 'Finances', 'Work & Business', '24.04', 'Dummy description')
    add_slug(CategoryModel, 'Job vacancies', 'Work & Business', '24.05', 'Dummy description')
    add_slug(CategoryModel, 'Profession', 'Work & Business', '24.06', 'Dummy description')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20150608_1126'),
    ]

    operations = [
        migrations.RunPython(create_category_slugs),
    ]
