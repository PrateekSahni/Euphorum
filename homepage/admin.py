from django.contrib import admin

# Register your models here.

from .models import Category, Topic, Post

admin.site.register(Category)
admin.site.register(Topic)
