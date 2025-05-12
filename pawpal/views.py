from django.shortcuts import render, get_object_or_404
from adopt.models import StrayAnimal

def homepage(request):
    animals = StrayAnimal.objects.filter(is_adopted=False)
    featured = animals[:3]
    total = animals.count()
    remaining = total - len(featured)

    return render(request, 'homepage.html', {
        'featured_animals': featured,
        'remaining_animals': remaining,
    })

def adopt(request):
    animals = StrayAnimal.objects.filter(is_adopted=False)
    return render(request, 'adopt.html', {'animals': animals})

def donate(request):
    urgent = StrayAnimal.objects.filter(is_adopted=False)[:4]
    return render(request, 'donate.html', {'urgent_animals': urgent})

def about(request):
    return render(request, 'about_us.html')

def favorites(request):
    # ตัวอย่างกรณีเก็บ favorites ไว้ใน session
    fav_ids = request.session.get('favorites', [])
    pets = StrayAnimal.objects.filter(id__in=fav_ids)
    return render(request, 'favorites.html', {'favorites': pets})

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def personality_test_view(request):
    return render(request, 'personality_test.html')

def pet_detail(request, pet_id):
    pet = get_object_or_404(StrayAnimal, id=pet_id)
    return render(request, 'pet_detail.html', {'pet': pet})

def sponsor(request):
    care_animals = StrayAnimal.objects.filter(is_adopted=False, is_sponsored=False)[:3]
    return render(request, 'homepage.html', {
    'featured_animals': animals,
    'sponsored_animals': sponsored,
    'care_animals': care_animals,
    'remaining_animals': StrayAnimal.objects.count() - animals.count()
    })