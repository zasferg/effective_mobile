from rest_framework.viewsets import ModelViewSet
from api.serializers import (
    BreedSerializer,
    BreedSerializerExtended,
    DogSerializer,
    AvgDataSerializer,
)
from api.models import Breed, Dog
from rest_framework.response import Response
from rest_framework import status
from api.services import get_breed_data, get_dog_data, get_dog_detail

class BreedViewSet(ModelViewSet):
    """
    ViewSet для управления данными о породах собак.
    """

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    def list(self, request):
        """
        Получает список всех пород собак с количеством собак каждой породы.

        Args:
            request (Request): HTTP запрос.

        Returns:
            Response: HTTP ответ с данными о породах собак.
        """
        try:
            breed_query = get_breed_data()
            serializer = BreedSerializerExtended(breed_query, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DogViewSet(ModelViewSet):
    """
    ViewSet для управления данными о собаках.
    """

    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def list(self, request):
        """
        Получает список всех собак и средний возраст собак каждой породы.

        Args:
            request (Request): HTTP запрос.

        Returns:
            Response: HTTP ответ с данными о собаках и среднем возрасте собак каждой породы.
        """
        try:
            queryset, dogs_breed_name_and_age = get_dog_data()
            dog_serialized_data = self.get_serializer(queryset, many=True)
            average_serializer = AvgDataSerializer(dogs_breed_name_and_age, many=True)

            response = {
                "dogs_data": dog_serialized_data.data,
                "average_age_per_breed": average_serializer.data,
            }

            return Response(response)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Получает данные о конкретной собаке и количество собак той же породы.

        Args:
            request (Request): HTTP запрос.
            pk (int): Первичный ключ (ID) собаки.

        Returns:
            Response: HTTP ответ с данными о конкретной собаке и количестве собак той же породы.
        """
        try:
            dog, breed_count = get_dog_detail(pk)
            dog_serialized_data = self.get_serializer(dog)

            response = {
                "dog_data": dog_serialized_data.data,
                "number_of_dogs_with_same_breed": breed_count,
            }

            return Response(response)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
