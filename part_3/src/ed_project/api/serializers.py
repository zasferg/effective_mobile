from api.models import *
from rest_framework import serializers

class BreedSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Breed.
    """

    class Meta:
        model = Breed
        fields = [
            "id",
            "name",
            "size",
            "frenliness",
            "trainability",
            "shedding_amount",
            "exersise_needs",
        ]

class BreedSerializerExtended(serializers.ModelSerializer):
    """
    Расширенный сериализатор для модели Breed, включающий количество собак данной породы.
    """

    count_of_dogs = serializers.CharField()

    class Meta:
        model = Breed
        fields = [
            "id",
            "name",
            "size",
            "frenliness",
            "trainability",
            "shedding_amount",
            "exersise_needs",
            "count_of_dogs",
        ]

class DogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Dog.
    """

    breed = BreedSerializer(read_only=True)
    breed_id = serializers.IntegerField()

    class Meta:
        model = Dog
        fields = [
            "id",
            "name",
            "age",
            "breed",
            "gender",
            "color",
            "favourite_food",
            "favourite_toy",
            "breed_id",
        ]

class AvgDataSerializer(serializers.Serializer):
    """
    Сериализатор для данных о среднем возрасте собак каждой породы.
    """

    breed_name = serializers.CharField()
    average_age = serializers.CharField()
