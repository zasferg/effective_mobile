from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import DogViewSet, BreedViewSet


router = DefaultRouter()


router.register(r"dogs", DogViewSet)
router.register(r"breeds", BreedViewSet)


urlpatterns = [path(r"", include(router.urls))]
