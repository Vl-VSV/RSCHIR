import random
from django.core.management.base import BaseCommand
from faker import Faker
from menu.models import MenuItem, Category

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми блюдами'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')  # Используем русский язык для генерации

        categories = [Category.HOT.value, Category.SOUP.value, Category.DESSERT.value, Category.SALAD.value, Category.DRINK.value]

        # Создание 100 блюд
        for _ in range(100):
            MenuItem.objects.create(
                name=fake.word().capitalize(),  # Случайное название
                description=fake.sentence(nb_words=10),  # Описание из 10 слов
                category=random.choice(categories),  # Случайная категория
                price=round(random.uniform(10, 500), 2)  # Случайная цена от 10 до 500
            )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена тестовыми блюдами'))