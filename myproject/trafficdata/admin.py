"""
CST8333 Programming Language Research Project
Practical Project Part 03
Student Name: Ka Yan Ieong
Student No.: 041070033
"""

# Register your models here.
from django.contrib import admin
from .models import DynamicTrafficVolume


@admin.register(DynamicTrafficVolume)
class DynamicTrafficVolumeAdmin(admin.ModelAdmin):
    list_display = ['get_data_display']

    def get_data_display(self, obj):
        data = obj.get_data()
        return f"{data.get('highway', 'N/A')} - {data.get('section', 'N/A')}"
