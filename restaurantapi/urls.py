from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import RestaurantViewSet, UserViewSet, VisitRatingViewSet, DateMatchViewSet, HasVisitedViewSet

router = routers.DefaultRouter()
router.register('restaurants', RestaurantViewSet)
router.register('users', UserViewSet)
router.register('ratings', VisitRatingViewSet)
router.register('current', DateMatchViewSet)
router.register('history', HasVisitedViewSet)

urlpatterns = [
  path('', include(router.urls)),
]
