from django.contrib import admin

# Register your models here.
from . models import Book,BookTracking

admin.site.register(Book)
admin.site.register(BookTracking)