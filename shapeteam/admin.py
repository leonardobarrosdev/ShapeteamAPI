from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(Exercise)
admin.site.register(NameExercise)
admin.site.register(Connection)
admin.site.register(Chat)
