from django.contrib import admin
from .models import Restaurant, HasVisited, VisitRating, DateMatch, MyUser

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Restaurant)
admin.site.register(HasVisited)
admin.site.register(VisitRating)
admin.site.register(DateMatch)