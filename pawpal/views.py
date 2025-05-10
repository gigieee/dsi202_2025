from django.shortcuts import render
from adopt.models import Animal

def homepage(request):
    animals = Animal.objects.all()[:6]
    return render(request, 'homepage.html', {'featured_animals': animals})

def adopt(request):
    animals = Animal.objects.filter(is_adopted=False)
    return render(request, 'adopt.html', {'animals': animals})

def donate(request):
    urgent = Animal.objects.filter(is_adopted=False)[:4]
    return render(request, 'donate.html', {'urgent_animals': urgent})

def about(request):
    return render(request, 'about_us.html')

def favorites(request):
    # ตัวอย่างกรณีเก็บ favorites ไว้ใน session
    fav_ids = request.session.get('favorites', [])
    pets = Animal.objects.filter(id__in=fav_ids)
    return render(request, 'favorites.html', {'favorites': pets})