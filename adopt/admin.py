from django.contrib import admin
from .models import StrayAnimal

@admin.register(StrayAnimal)
class StrayAnimalAdmin(admin.ModelAdmin):
    list_display = ('pet_id', 'name', 'breed', 'species', 'is_adopted')
    ordering = ['pet_id']  # เรียงตาม pet_id จากน้อยไปมาก
    search_fields = ['name', 'breed', 'pet_id']
    list_filter = ['species', 'size', 'gender']