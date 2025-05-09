from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db import models  # ✅ เพิ่มบรรทัดนี้!
from .models import Pet

def home(request):
    return render(request, 'home.html')
class PetListView(ListView):
    model = Pet
    template_name = 'pet_list.html'
    context_object_name = 'pets'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        gender = self.request.GET.get('gender')
        breed = self.request.GET.get('breed')
        age = self.request.GET.get('age')

        if q:
            queryset = queryset.filter(
                models.Q(name__icontains=q) |
                models.Q(breed__icontains=q)
            )
        if gender:
            queryset = queryset.filter(gender=gender)
        if breed:
            queryset = queryset.filter(breed__icontains=breed)
        if age:
            queryset = queryset.filter(age=age)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_gender'] = self.request.GET.get('gender', '')
        context['selected_breed'] = self.request.GET.get('breed', '')
        context['selected_age'] = self.request.GET.get('age', '')
        return context
class PetDetailView(DetailView):
    model = Pet
    template_name = 'pet_detail.html'
    context_object_name = 'pet'