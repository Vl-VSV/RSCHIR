import random
from django.core.management.base import BaseCommand, CommandParser
from faker import Faker
from faker_food import FoodProvider
from menu.models import MenuItem, Category

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми блюдами'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить базу перед заполнением (по умолчанию: False)',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Количество генерируемых блюд (по умолчанию: 100)'
        )
        parser.add_argument(
            '--price-step',
            type=int,
            default=50,
            help='Шаг генерации цены (по умолчанию: 50)'
        )
    
    def handle(self, *args, **kwargs):
        clear_database = kwargs['clear']
        count = kwargs['count']
        price_step = kwargs['price_step']
        
        if clear_database:
            MenuItem.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('База данных очищена'))
            
        fake = Faker('ru_RU')
        fake.add_provider(FoodProvider)

        categories = [Category.HOT.value, Category.SOUP.value, Category.DESSERT.value, Category.SALAD.value, Category.DRINK.value]

        for _ in range(count):
            MenuItem.objects.create(
                name=fake.dish(), 
                description=fake.dish_description(),
                category=random.choice(categories),
                price=round(random.randrange(250, 4501, price_step))
            )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена тестовыми блюдами'))