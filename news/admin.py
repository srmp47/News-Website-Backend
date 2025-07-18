from django.contrib import admin

# Register your models here.
from .models import News,Tag
admin.site.register(News)
admin.site.register(Tag)