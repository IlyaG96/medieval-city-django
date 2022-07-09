import random

from more_itertools import chunked

from django_seed import Seed
from django.core.management.base import BaseCommand
from medieval_city.models import Civilian, Estate, Vassal, City

seeder = Seed.seeder()

TOTAL_POPULATION_COUNT = 500
BASE_INCOME = 100
CITY_NAME = 'Мидгард'
ESTATES = [
    'Король',
    'Граф',
    'Герцог',
    'Рыцарь',
    'Крестьянин'
]

WOMEN_NAMES = [
    'Аврора',
    'Агнессa',
    'Анна',
    'Беатрис',
    'Батильда',
    'Вертэнди',
    'Вендая',
    'Вилфреда',
    'Габриэлла',
    'Далила',
    'Девнет',
    'Джакобина',
    'Ернестайн',
    'Ерания',
    'Жонкилия',
    'Зандра',
    'Зибилла',
    'Зэодосия',
    'Илинн',
    'Имогин',
    'Иоланда',
    'Камилла',
    'Карамия',
    'Кармэль',
    'Кризанта',
    'Лаверн',
    'Лакретия',
    'Мабелла',
    'Мадонна',
    'Малинда',
]

MAN_NAMES = [
    'Ааррон',
    'Абрахам',
    'Азэлстан',
    'Алгар',
    'Байярд',
    'Бардолф',
    'Беорегард',
    'Валентайн',
    'Вард',
    'Вилберн',
    'Вольф',
    'Габриэль',
    'Гарольд',
    'Глендауэр',
    'Даймонд',
    'Дариан',
    'Деметриус',
    'Ирвинг',
    'Каллен',
    'Киллиан',
    'Кристофер',
    'Леонард',
    'Людовик',
    'Мариус',
    'Миллард',
    'Николас',
    'Олдред',
    'Оллгар',
    'Освальд',
    'Персиваль',
    'Реджинальд',
    'Роуланд',
    'Теобальд'
]

SURNAMES = [
    'Авалос',
    'Адельманн',
    'Альбре',
    'Анжера',
    'Жуайез',
    'Лаведан',
    'Ланьяк',
    'Гелдер',
    'Говард',
    'Грумо',
    'Далкейт',
    'Драго',
    'Диоклей',
    'Дюплесси',
    'Савелли',
    'Сальчи',
    'Cан-Элия',
    'Саффолк',
    'Степлтон',
    'Стюарт',
    'Суассон',
    'Тауншенд',
    'Тревизо',
    'Труа',
    'Уотефорд',
    'Уиллоуби',
    'Фериа',
    'Флеминг',
    'Форино',
    'Фицджеймс',
    'Карлайл',
    'Карпинето',
    'Кассано',
    'Коллато',
    'Саган',
    'Сиано',
    'Салерно'
]


def create_estates():
    for estate in ESTATES:
        seeder.add_entity(
            Estate, 1, {
                'class_name': estate
            }
        )
        seeder.execute()


def create_city():
    seeder.add_entity(
        City, 1, {
            'name': CITY_NAME
        }
    )
    seeder.execute()


def create_civilians():
    total_civilians = 0
    estates = Estate.objects.all()
    city = City.objects.first()
    # create king, some hardcode :D
    seeder.add_entity(
        Civilian, 1, {
            'name': lambda x: random.choice(MAN_NAMES + WOMEN_NAMES),
            'surname': lambda x: random.choice(SURNAMES),
            'age': lambda x: random.randint(30, 65),
            'estate': estates[0],  # first is the king, right?
            'income': BASE_INCOME * TOTAL_POPULATION_COUNT,
            'city': city
        },
    )
    seeder.execute()
    estates_without_king = estates[1:]
    estates_quantity = estates.count()

    total_civilians += 1
    # create last estate civilians
    for estate_num, estate in enumerate(estates_without_king):
        estate = estate
        income = (estates_quantity - estate_num + 1) * BASE_INCOME
        if estate_num == len(estates_without_king) - 1:
            for civilian in range(TOTAL_POPULATION_COUNT - total_civilians):
                seeder.add_entity(
                    Civilian, 1, {
                        'name': lambda x: random.choice(MAN_NAMES + WOMEN_NAMES),
                        'surname': lambda x: random.choice(SURNAMES),
                        'age': lambda x: random.randint(0, 65),
                        'estate': estate,
                        'income': income,
                        'city': city
                    },
                )
                seeder.execute()
                total_civilians += 1
        else:
            for civilian in range(1, (estate_num + 2) ** 2):
                seeder.add_entity(
                    Civilian, 1, {
                        'name': lambda x: random.choice(MAN_NAMES + WOMEN_NAMES),
                        'surname': lambda x: random.choice(SURNAMES),
                        'age': lambda x: random.randint(0, 65),
                        'estate': estate,
                        'income': income,
                        'city': city
                    },
                )
                seeder.execute()
                total_civilians += 1


def create_relations():
    estates = Estate.objects.all()
    kings_estate = estates.first()
    last_estate = estates.last()
    for index, estate in enumerate(estates):
        if estate == kings_estate:  # dedicated creation for the king
            king = Civilian.objects.get(estate=kings_estate)
            vassals = estates[index + 1].civilians.all()
            for vassal in vassals:
                vassal, created = Vassal.objects.get_or_create(
                    subordinate=vassal
                )
                king.vassal.add(vassal)
            king.save()

        elif estate == last_estate:
            civilians = estate.civilians.all()
            seniors = estates[index - 1].civilians.all()
            civilians_count = civilians.count()
            seniors_count = seniors.count()

            civilians_groups = list(
                chunked(civilians,
                        n=int(round((civilians_count / seniors_count)))))
            for group, civilians_group in enumerate(civilians_groups):
                for civilian in civilians_group:
                    civilian.senior = seniors[group]
                    civilian.save()

        else:
            civilians = estate.civilians.all()
            seniors = estates[index - 1].civilians.all()
            vassals = estates[index + 1].civilians.all()

            civilians_count = civilians.count()
            vassals_count = vassals.count()
            seniors_count = seniors.count()
            vassals_groups = list(
                chunked(vassals,
                        n=int(round((vassals_count / civilians_count)))))
            civilians_groups = list(
                chunked(civilians,
                        n=int(round((civilians_count / seniors_count)))))

            for group_num, civilian in enumerate(civilians):
                for group_index, grouped_vassal in enumerate(vassals_groups[group_num]):
                    vassal, created = Vassal.objects.get_or_create(
                        subordinate=grouped_vassal
                    )
                    civilian.vassal.add(vassal)
                    civilian.save()
            for group, civilians_group in enumerate(civilians_groups):
                for civilian in civilians_group:
                    civilian.senior = seniors[group]
                    civilian.save()


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_city()
        create_estates()
        create_civilians()
        create_relations()
