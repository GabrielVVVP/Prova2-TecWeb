from django.contrib import admin
from .models import Station, Parameter, User 

admin.site.register(User)
admin.site.register(Station)
admin.site.register(Parameter)

