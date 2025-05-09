from django.urls import path
from . import views
from .views import PetListView, PetDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', PetListView.as_view(), name='pet-list'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet-detail'),
]