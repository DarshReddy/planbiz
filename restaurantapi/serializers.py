from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Restaurant, HasVisited, VisitRating, DateMatch, MyUser


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = MyUser
    fields = ('id', 'email', 'password','is_female','img_url','avg_rating')
    extra_kwargs = {'password': {'write_only': True,
    'required': True}}

  
  def create(self, validated_data):
    user = MyUser.objects.create_user(**validated_data)
    Token.objects.create(user=user)
    return user

class RestaurantSerializer(serializers.ModelSerializer):
  class Meta:
    model = Restaurant
    fields = ('resID', 'Name', 'Url', 'Locality', 'Avg_cost', 'Cuisines', 'Img_url','no_dates')

class HasVisitedSerializer(serializers.ModelSerializer):
  rest = serializers.SerializerMethodField()

  class Meta:
    model = HasVisited
    fields = ('id','user','restaurant','dayofvisit','rest')

  def get_rest(self, obj):
    try:
      rest = Restaurant.objects.get(resID=obj.restaurant.resID)
      return RestaurantSerializer(rest).data
    except Exception as e:
      return {}

class VisitRatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = VisitRating
    fields = ('id','guy', 'girl', 'rated_date', 'rating1', 'rating2', 'dayofvisit')

class DateMatchSerializer(serializers.ModelSerializer):
  male = serializers.SerializerMethodField()
  female = serializers.SerializerMethodField()

  class Meta:
    model = DateMatch
    fields = ('id','guy', 'girl', 'restaurant', 'dateaccepted','timeofvisit', 'female', 'male')

  def get_male(self, obj):
    try:
      male = MyUser.objects.get(email=obj.guy)
      return UserSerializer(male).data
    except Exception as e:
      return {}
  
  def get_female(self, obj):
    try:
      female = MyUser.objects.get(email=obj.girl)
      return UserSerializer(female).data
    except Exception as e:
      return {}


