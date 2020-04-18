from datetime import datetime, timedelta
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import DateMatch, HasVisited, MyUser, Restaurant, VisitRating, MyUser
from .serializers import (DateMatchSerializer, HasVisitedSerializer,
                          RestaurantSerializer, UserSerializer,
                          VisitRatingSerializer)
from .pyzom import Exjson, GetRst


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class RestaurantViewSet(viewsets.ModelViewSet):
  queryset = Restaurant.objects.all()
  serializer_class = RestaurantSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,) 

class HasVisitedViewSet(viewsets.ModelViewSet):
  queryset = HasVisited.objects.all()
  serializer_class = HasVisitedSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def create(self, request, *args, **kwargs):
    if 'restaurant' in request.data:
      user = request.user
      restaurant = Restaurant.objects.get(resID=request.data['restaurant'])
      dayofvisit = timezone.now()
      visit = HasVisited.objects.create(user=user,restaurant=restaurant,dayofvisit=dayofvisit)
      serializer = HasVisitedSerializer(visit, many=False)
      response = {'message': 'Visit Updated', 'result': serializer.data}
      return Response(response, status=status.HTTP_200_OK)
    else:
      response = {'message': 'you need to provide restaurant'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)

  @action(detail=False, methods=['POST','GET'])
  def get_visits(self, request):
    user = request.user
    visit = HasVisited.objects.filter(user=user)
    if 'lat' and 'lon' in request.data:
      if 'bgt' in request.data:
        rsts = GetRst.getRsts(float(request.data['lat']), float(request.data['lon']), float(request.data['bgt']))
      else:
        rsts = GetRst.getRsts(float(request.data['lat']), float(request.data['lon']))

      rs_del = []
      for i in range(len(rsts)):
        for v in visit:
          if int(rsts[i]['resID']) == v.restaurant.resID:
            rs_del.append(rsts[i])
      rsts = [item for item in rsts if item not in rs_del]
      response = {'nearby_restaurants': rsts}
      return Response(response, status=status.HTTP_200_OK)
    else:
      response = {'message':'could not fetch restaurants'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)



class VisitRatingViewSet(viewsets.ModelViewSet):
  queryset = VisitRating.objects.all()
  serializer_class = VisitRatingSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  @action(detail=False, methods=['POST'])
  def rate_now(self, request, pk=None):
    if 'rated_date' and 'stars' in request.data:
      date = DateMatch.objects.get(id=request.data['rated_date'])
      try:
        rating = VisitRating.objects.get(rated_date=date)
        if request.user.is_female:
          rating.girl = request.user
          rating.rating2 = request.data['stars']
        else:
          rating.guy = request.user
          rating.rating1 = request.data['stars']
        serializer = VisitRatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)
      except:
        if request.user.is_female:
          rating = VisitRating.objects.create(rating2=request.data['stars'], rated_date=date)
        else:
          rating = VisitRating.objects.create(rating1=request.data['stars'], rated_date=date)
        serializer = VisitRatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      response = {'message': 'Please provide all details'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)

class DateMatchViewSet(viewsets.ModelViewSet):
  queryset = DateMatch.objects.all()
  serializer_class = DateMatchSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def create(self, request, *args, **kwargs):

    if 'restaurant' in request.data:
      rst = Restaurant.objects.get(resID=request.data['restaurant'])
      if request.user.is_female: 
        datematch = DateMatch.objects.create(girl=request.user,restaurant=rst)
        serializer = DateMatchSerializer(datematch)
        response = {'message': 'Date Created', 'result': serializer.data}
        return Response(response, status=status.HTTP_201_CREATED)
      else:
        datematch = DateMatch.objects.create(guy=request.user,restaurant=rst)
        serializer = DateMatchSerializer(datematch)
        response = {'message': 'Date Created', 'result': serializer.data}
        return Response(response, status=status.HTTP_201_CREATED)
    else:
      response = {'message': 'Please provide all details'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
  @action(detail=False,methods=['POST'])
  def check_dates(self, request, *args, **kwargs):

    if 'restaurant' in request.data:
      rst = Restaurant.objects.get(resID=request.data['restaurant'])
      dates = DateMatch.objects.filter(restaurant=rst)
      time = datetime.now() - timedelta(hours=1)
      dates = dates.filter(timeofvisit__gte = time)

      if request.user.is_female:
        dates = dates.filter(dateaccepted = False).exclude(guy = None)
      else:
        dates = dates.filter(dateaccepted = False).exclude(girl = None)

      if len(dates)!=0:
        serializer = DateMatchSerializer(dates, many=True)
        response = {'dates': serializer.data}
        return Response(response, status=status.HTTP_200_OK)
      else:
        print("create")
        return DateMatchViewSet.create(self, request)
    else:
      response = {'message': 'Provide restaurant details'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)

  @action(detail=True, methods=['POST'])
  def accept_date(self, request, pk=None):

    date = DateMatch.objects.get(id=pk)
    date.dateaccepted = True
    if request.user.is_female:
      date.girl = request.user
    else:
      date.guy = request.user
    try:
      vserializer = VisitRatingSerializer(VisitRating.objects.get(rated_date=date))
    except:
      visit = VisitRating.objects.create(guy=date.guy, girl=date.girl, rated_date=date)
      vserializer = VisitRatingSerializer(visit)
      
    serializer = DateMatchSerializer(date)
    response = {'message': 'Date accepted','result': serializer.data, 'rating': vserializer.data }
    return Response(response, status=status.HTTP_200_OK)
