from model_mommy.recipe import Recipe
from core.models import ChHive


hive_1 = Recipe(
    ChHive,
    name='John Doe',
    nickname='joe',
    age=18,
    birthday=date.today(),
    appointment=datetime.now()
)