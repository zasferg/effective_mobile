from django.db import models
from ed_project.api.validators import range_validate, friendliness_text_validate
from django.db.models import Manager


class Dog(models.Model):
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
