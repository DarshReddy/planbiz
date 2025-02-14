from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.conf import settings
from fcm_django.models import FCMDevice
from django.utils.translation import ugettext_lazy as _ 

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, is_female, password=None):
        if not email:
            raise ValueError('Users must have an username')

        user = self.model(
            email = email,
            is_female = is_female,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, is_female, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            is_female=is_female,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyValidator(UnicodeUsernameValidator):
  regex = r'^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$'

class MyUser(AbstractBaseUser):
  username_validator = MyValidator()
  email = models.CharField(
      _('username'),
      max_length=150,
      unique=True,
      help_text=_('Instagram like username.'),
      validators=[username_validator],
          error_messages={
          'unique': _("A user with that username already exists."),
      },
  )
  phone = models.CharField(max_length=32,unique=True,null=True)
  is_female = models.BooleanField(default=False)
  img_url = models.TextField(blank=True,max_length=512)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)

  objects = MyUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['is_female']

  def __str__(self):
        return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return True

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin

  def avg_rating(self):
    sum_rating = 0
    if(self.is_female):
      ratings = VisitRating.objects.filter(girl=self,rating1__gte=1)
      for rating in ratings:
        sum_rating += rating.rating2
    else:
      ratings = VisitRating.objects.filter(guy=self,rating2__gte=1)
      for rating in ratings:
        sum_rating += rating.rating1
    if len(ratings) > 0:
      return sum_rating / len(ratings)
    else:
      return 0

class Restaurant(models.Model):
  resID = models.IntegerField(primary_key=True)
  Name = models.CharField(max_length=32)
  Url = models.CharField(max_length=256)
  Locality = models.CharField(max_length=128)
  Avg_cost = models.IntegerField()
  Cuisines = models.CharField(max_length=256)
  Img_url = models.CharField(max_length=256, blank=True)
  Rating = models.FloatField(max_length=256, default=0.0)

  def no_dates(self):
    dates = DateMatch.objects.filter(restaurant=self)
    return len(dates)

class HasVisited(models.Model):
  user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  dayofvisit = models.DateTimeField(editable=False)
  def save(self, *args, **kwargs):
    self.dayofvisit = timezone.now()
    return super(HasVisited, self).save(*args, **kwargs)

class DateMatch(models.Model):
  guy = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='guy', default=None, null=True)
  girl = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='girl', default=None, null=True)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,default=None)
  dateaccepted = models.BooleanField(default=False)
  timeofvisit = models.TimeField(auto_now=True, editable=False)

class VisitRating(models.Model):
  guy = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='guyrated', default=None, null=True)
  girl = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='girlrated', default=None, null=True)
  rated_date = models.ForeignKey(DateMatch, on_delete=models.SET_NULL, null=True)
  rating1 = models.IntegerField(default=0,validators=[MinValueValidator(1),MaxValueValidator(5)])
  rating2 = models.IntegerField(default=0,validators=[MinValueValidator(1),MaxValueValidator(5)])
  dayofvisit = models.DateTimeField(auto_now=True)