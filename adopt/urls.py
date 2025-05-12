from django.urls import path
from . import views

urlpatterns = [
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pet/<int:pet_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]