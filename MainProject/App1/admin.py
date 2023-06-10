from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import myModel  #added

admin.site.register(myModel)  #added
