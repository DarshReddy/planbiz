from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.conf import settings
from fcm_django.models import FCMDevice

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, is_female, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
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

class MyUser(AbstractBaseUser):
  email = models.EmailField(max_length=255,unique=True,default='email@mail.com')
  is_female = models.BooleanField(default=False)
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
      ratings = VisitRating.objects.filter(girl=self)
      for rating in ratings:
        sum_rating += rating.rating2
    else:
      ratings = VisitRating.objects.filter(guy=self)
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