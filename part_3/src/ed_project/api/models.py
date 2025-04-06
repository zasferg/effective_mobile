from django.db import models
from api.validators import range_validate, friendliness_text_validate
from django.db.models import Manager

class Dog(models.Model):
    """
    Модель для представления данных о собаках.

    Attributes:
        name (str): Имя собаки.
        age (int): Возраст собаки.
        breed (ForeignKey): Порода собаки.
        gender (str): Пол собаки.
        color (str): Цвет собаки.
        favourite_food (str): Любимая еда собаки.
        favourite_toy (str): Любимая игрушка собаки.
    """

    name = models.CharField()
    age = models.IntegerField()
    breed = models.ForeignKey("Breed", related_name="breed", on_delete=models.CASCADE)
    gender = models.CharField()
    color = models.CharField()
    favourite_food = models.CharField()
    favourite_toy = models.CharField()

    def __str__(self):
        return f"{self.name}, {self.age}, {self.breed}"

class Breed(models.Model):
    """
    Модель для представления данных о породах собак.

    Attributes:
        name (str): Название породы.
        size (str): Размер породы.
        frenliness (int): Дружелюбность породы.
        trainability (int): Обучаемость породы.
        shedding_amount (int): Количество линьки породы.
        exersise_needs (int): Потребности в упражнениях породы.
    """

    name = models.CharField()
    size = models.CharField(
        max_length=10,
        choices=(
            ("Tiny", "Tiny"),
            ("Small", "Small"),
            ("Medium", "Medium"),
            ("Large", "Large"),
        ),
        validators=[
            friendliness_text_validate,
        ],
    )
    frenliness = models.IntegerField(
        validators=[
            range_validate,
        ]
    )
    trainability = models.IntegerField(
        validators=[
            range_validate,
        ]
    )
    shedding_amount = models.IntegerField(
        validators=[
            range_validate,
        ]
    )
    exersise_needs = models.IntegerField(
        validators=[
            range_validate,
        ]
    )
