from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Restaurant, HasVisited, VisitRating, DateMatch, MyUser


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = MyUser
    fields = ('id', 'email', 'password','is_female')
    extra_kwargs = {'password': {'write_only': True,
    'required': True}}

  
  def create(self, validated_data):
    user = MyUser.objects.create_user(**validated_data)
    Token.objects.create(user=user)
    return user

class RestaurantSerializer(serializers.ModelSerializer):
  class Meta:
    model = Restaurant
    fields = ('resID', 'Name', 'Url', 'Locality', 'Avg_cost', 'Cuisines', 'Img_url')

class HasVisitedSerializer(serializers.ModelSerializer):
  class Meta:
    model = HasVisited
    fields = ('id','user','restaurant','dayofvisit')

class VisitRatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = VisitRating
    fields = ('id','guy', 'girl', 'rated_date', 'rating1', 'rating2', 'dayofvisit')

class DateMatchSerializer(serializers.ModelSerializer):
  class Meta:
    model = DateMatch
    fields = ('id','guy', 'girl', 'restaurant', 'dateaccepted','timeofvisit')


