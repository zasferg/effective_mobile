from api.models import Breed, Dog
from django.db.models import Avg, OuterRef, Subquery, Count

def get_breed_data():
    """
    Получает данные о породах собак, включая количество собак каждой породы.

    Returns:
        QuerySet: Запрос с аннотированными данными о породах и количестве собак каждой породы.
    """
    dog_count = (
        Dog.objects.filter(breed_id=OuterRef("id"))
        .values("breed_id")
        .annotate(count=Count("breed_id"))
        .values("count")
    )
    breed_query = Breed.objects.annotate(
        count_of_dogs=Subquery(dog_count)
    ).values()
    return breed_query

def get_dog_data():
    """
    Получает данные о собаках и средний возраст собак каждой породы.

    Returns:
        tuple: Кортеж, содержащий QuerySet с данными о собаках и QuerySet со средним возрастом собак каждой породы.
    """
    queryset = Dog.objects.all()
    breed_name_subquery = Breed.objects.filter(id=OuterRef("breed_id")).values("name")
    dogs_breed_name_and_age = (
        Dog.objects.annotate(breed_name=Subquery(breed_name_subquery))
        .values("breed_name")
        .annotate(average_age=Avg("age"))
    )
    return queryset, dogs_breed_name_and_age

def get_dog_detail(pk):
    """
    Получает данные о конкретной собаке и количество собак той же породы.

    Args:
        pk (int): Первичный ключ (ID) собаки.

    Returns:
        tuple: Кортеж, содержащий объект собаки и количество собак той же породы.
    """
    dog = Dog.objects.get(pk=pk)
    breed_count = Dog.objects.filter(breed_id=dog.breed_id).count()
    return dog, breed_count
