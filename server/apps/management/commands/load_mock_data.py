from datetime import timedelta
from random import randint

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from faker import Faker

from server.apps.collects.models import Collect, Occasion
from server.apps.payment.models import Payment


User = get_user_model()
# Создание генератора фейковых данных
fake = Faker()

# Определение команды
class Command(BaseCommand):
    help = "Fill the database with test data"

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.WARNING(
                "Start filling database with test data."
            )
        )
        self.stdout.write(
            "Data is generated random way so payment and occasion "
            "amounts may be different"
        )
        self.stdout.write(
            self.style.WARNING("Test emails will not be sent")
        )
        # Создание поводов
        occasions = [
            Occasion.objects.create(name=fake.word()) for _ in range(20)
        ]

        # Создание пользователей
        users = []
        for i in range(400):
            # Добавим индекс к email, чтобы были уникальные
            email = f"user{i}_{fake.email()}"
            user = User.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=email,
                password="SuperSecretPassword",
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS("Users are generated"))

        # Создание сборов
        collects = []
        for _ in range(100):
            collect = Collect.objects.create(
                author=fake.random_element(users),
                name=fake.sentence(nb_words=4),
                occasion=fake.random_element(occasions),
                description=fake.text(),
                final_sum=fake.random_number(digits=6),
                completion_datetime=now() + timedelta(days=randint(1, 365))
            )
            collects.append(collect)

        self.stdout.write(self.style.SUCCESS("Collects are created"))

        # Создание платежей
        for _ in range(5000):
            Payment.objects.create(
                contributor=fake.random_element(users),
                collect=fake.random_element(collects),
                sum=randint(10, 1000)
            )
            self.stdout.write(self.style.SUCCESS("Payments are created"))
        self.stdout.write(self.style.SUCCESS("Test data are created successfully!"))
