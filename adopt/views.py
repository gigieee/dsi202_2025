from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import StrayAnimal

def pet_detail(request, pet_id):
    pet = get_object_or_404(StrayAnimal, id=pet_id)
    favorites = request.session.get('favorites', [])
    is_favorited = pet_id in favorites
    return render(request, 'pet_detail.html', {'pet': pet, 'is_favorited': is_favorited})

def toggle_favorite(request, pet_id):
    favorites = request.session.get('favorites', [])
    if pet_id in favorites:
        favorites.remove(pet_id)
    else:
        favorites.append(pet_id)
    request.session['favorites'] = favorites
    return redirect('pet_detail', pet_id=pet_id)