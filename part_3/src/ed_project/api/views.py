from rest_framework.viewsets import ModelViewSet
from api.serializers import (
    BreedSerializer,
    BreedSerializerExtended,
    DogSerializer,
    AvgDataSerializer,
)
from api.models import Breed, Dog
from rest_framework.response import Response
from django.db.models import Avg, OuterRef, Subquery, Count
from rest_framework import status


class BreedViewSet(ModelViewSet):

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    def list(self, request):
        try:
            dog_count = (
                Dog.objects.filter(breed_id=OuterRef("id"))
                .values("breed_id")
                .annotate(count=Count("breed_id"))
                .values("count")
            )
            breed_query = Breed.objects.annotate(
                count_of_dogs=Subquery(dog_count)
            ).values()
            serializer = BreedSerializerExtended(breed_query, many=True)

            return Response(serializer.data)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DogViewSet(ModelViewSet):

    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def list(self, request):

        try:
            queryset = self.get_queryset()
            dog_serialized_data = self.get_serializer(queryset, many=True)

            breed_name_subquery = Breed.objects.filter(id=OuterRef("breed_id")).values(
                "name"
            )
            dogs_breed_name_and_age = (
                Dog.objects.annotate(breed_name=Subquery(breed_name_subquery))
                .values("breed_name")
                .annotate(average_age=Avg("age"))
            )
            average_serializer = AvgDataSerializer(dogs_breed_name_and_age, many=True)

            response = {
                "dogs_data": dog_serialized_data.data,
                "average_age_per_breed": average_serializer.data,
            }

            return Response(response)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:

            dog = Dog.objects.get(pk=pk)
            dog_serialized_data = self.get_serializer(dog)
            breed_count = Dog.objects.filter(breed_id=dog.breed_id).count()

            response = {
                "dog_data": dog_serialized_data.data,
                "number_of_dogs_with_same_breed": breed_count,
            }

            return Response(response)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
