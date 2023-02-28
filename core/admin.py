from django.contrib import admin
from .models import Point

@admin.register(Point)
class Point(admin.ModelAdmin):
    
    list_display = ('staff', 'head', 'value', 'month', 'year',)
    list_filter = ('staff', 'head', 'year', 'month')
    search_fields = ('value',)
    

# Register your models here.
