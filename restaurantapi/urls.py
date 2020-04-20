from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .views import RestaurantViewSet, UserViewSet, VisitRatingViewSet, DateMatchViewSet, HasVisitedViewSet, CustomAuthToken

router = routers.DefaultRouter()
router.register('restaurants', RestaurantViewSet)
router.register('users', UserViewSet)
router.register('ratings', VisitRatingViewSet)
router.register('current', DateMatchViewSet)
router.register('history', HasVisitedViewSet)
router.register('devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
  path('', include(router.urls)),
  url(r'^auth/', CustomAuthToken.as_view()),
]
