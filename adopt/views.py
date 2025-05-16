#Import
from django.shortcuts import render, redirect, get_object_or_404
from .models import StrayAnimal, GeneralDonation, MedicalSponsorship, AdoptionRequest, Blog, Notification, SponsorshipDonation, MedicalDonation, PersonalityResult, FavoritePet, RecentlyViewedPet
from .forms import GeneralDonationForm, SponsorshipDonationForm, AdoptionRequestForm, MedicalDonationForm, CustomSignupForm, CustomLoginForm
from django.http import JsonResponse, Http404, HttpResponse
from django.db.models import Sum, Q, Count
from django.template.loader import render_to_string
from collections import defaultdict
import json
import urllib.parse
from urllib.parse import unquote_plus
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adopt.utils import generate_promptpay_qr_image_base64
from django.views.decorators.csrf import csrf_exempt
import base64
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout, get_backends
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Dash board
@login_required
def user_dashboard(request):
    user = request.user

    # 🧠 Personality test result
    personality_result = PersonalityResult.objects.filter(user=user).first()

    # 👀 Recently viewed pets (stored in session)
    favorite_pets = FavoritePet.objects.filter(user=request.user).select_related('pet')
    

    # 📄 Adoption requests
    adoption_requests = AdoptionRequest.objects.filter(user=user)

    # 💰 Donations
    general_donations = GeneralDonation.objects.filter(user=request.user)
    medical_donations = MedicalDonation.objects.filter(user=request.user)
    sponsorship_donations = SponsorshipDonation.objects.filter(user=request.user)

    return render(request, 'user_dashboard.html', {
        'personality_result': personality_result,
        'favorite_pets': [f.pet for f in favorite_pets],
        'adoption_requests': adoption_requests,
        'general_donations': general_donations,
        'medical_donations': medical_donations,
        'sponsorship_donations': sponsorship_donations
    })

# Heart Fav
@csrf_exempt
@login_required
def toggle_favorite(request, pet_id):
    if request.method == 'POST':
        pet = get_object_or_404(StrayAnimal, id=pet_id)
        fav, created = FavoritePet.objects.get_or_create(user=request.user, pet=pet)
        if not created:
            fav.delete()
        return JsonResponse({'status': 'ok'})

@csrf_exempt
@login_required
def add_recently_viewed(request, pet_id):
    if request.method == "POST":
        pet = get_object_or_404(StrayAnimal, id=pet_id)
        RecentlyViewedPet.objects.update_or_create(
            user=request.user, pet=pet,
            defaults={'viewed_at': timezone.now()}
        )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid method"}, status=405)

def homepage(request):
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
    # Available Pets including Medical Pets
    all_available_pets = StrayAnimal.objects.filter(is_adopted=False)
    featured = all_available_pets[:4]
    #total = all_available_pets.count()
    remaining = all_available_pets.count() - len(featured)

    #sponsored_animals = StrayAnimal.objects.filter(is_adopted=False, id__in=medical_pet_ids)

    # Section: Support Care for Our PawFriends (exclude medical pet)
    # เอา id ของสัตว์ที่มี medical support
    medical_pet_ids = MedicalSponsorship.objects.values_list('pet_id', flat=True)
    support_animals = StrayAnimal.objects.filter(
        is_adopted=False
    ).exclude(id__in=medical_pet_ids)[:5]

    return render(request, 'homepage.html', {
        'available_pets': all_available_pets,
        'featured_animals': featured,
        'remaining_animals': remaining,
        'support_animals': support_animals,
        'unread_notif_count': unread_count,
    })


def donate(request):
    urgent = StrayAnimal.objects.filter(is_adopted=False)[:4]
    sponsorships = MedicalSponsorship.objects.filter(is_active=True)
    return render(request, 'donate.html', {
        'urgent_animals': urgent,
        'sponsorships': sponsorships
    })

def about_us(request):
    adopted_count = StrayAnimal.objects.filter(is_adopted=True).count()
    medical_count = MedicalSponsorship.objects.count()
    donation_total = GeneralDonation.objects.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'about_us.html', {
        'adopted_count': adopted_count,
        'medical_count': medical_count,
        'donation_total': donation_total,
    })

def favorites_view(request):
    return render(request, 'favorites.html')

def get_favorite_pets(request):
    pet_ids = FavoritePet.objects.filter(user=request.user).values_list('pet_id', flat=True)
    pets = StrayAnimal.objects.filter(id__in=pet_ids)
    data = []

    for pet in pets:
        data.append({
            "id": pet.id,
            "pet_id": pet.pet_id,
            "name": pet.name,
            "breed": pet.breed,
            "gender": pet.gender,
            "age": f"{pet.age_value} {pet.age_unit}",
            "personality": pet.behavior,
            "image_url": pet.image.url
        })
    return JsonResponse({"pets": data})

    for fav in favorites:
        pet = fav.pet
        data.append({
            "id": pet.id,
            "pet_id": pet.pet_id,
            "name": pet.name,
            "breed": pet.breed,
            "gender": pet.gender,
            "age": f"{pet.age_value} {pet.age_unit}",
            "personality": pet.behavior,
            "image_url": pet.image.url
        })

    return JsonResponse({"pets": data})


# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if password1 != password2:
            return render(request, 'signup.html', {'error': "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': "Username already exists"})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': "Email already in use"})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        return redirect('login')  # ไปหน้า log in ต่อเลย
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def custom_logout_view(request):
    logout(request)
    return redirect('homepage')  

def personality_test_view(request):
    return render(request, 'personality_test.html')


#หน้า Overview Donate
def general_donate(request):
    if request.method == 'POST':
        donor_name = request.POST.get("donor_name")
        email = request.POST.get("email")
        payment_method = request.POST.get("payment_method")  # อาจจะลบทิ้งถ้าไม่ใช้
        amount = request.POST.get("amount")
        message = request.POST.get("message")
        slip_image = request.FILES.get("slip_image")

        try:
            donation = GeneralDonation.objects.create(
                donor_name=donor_name,
                email=email,
                amount=amount,
                message=message,
                slip_image=slip_image,
                user=request.user if request.user.is_authenticated else None
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
# หน้าแสดงรายการ sponsorship
def medical_sponsorship_list(request):
    sponsorships = MedicalSponsorship.objects.filter(is_active=True)
    return render(request, 'sponsorship_list.html', {'sponsorships': sponsorships})

# หน้ารายละเอียดและแบบฟอร์มบริจาคเฉพาะสัตว์
def medical_sponsorship_detail(request, sponsorship_id):
    sponsorship = get_object_or_404(MedicalSponsorship, id=sponsorship_id)
    return render(request, 'sponsorship_detail.html', {
        'sponsorship': sponsorship,
    })

@csrf_exempt
def medical_donate(request, sponsorship_id):
    sponsorship = get_object_or_404(MedicalSponsorship, id=sponsorship_id)

    if request.method == "POST":
        form = MedicalDonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.sponsorship = sponsorship
            if request.user.is_authenticated:
                donation.user = request.user  # ✅ เพิ่มตรงนี้
            donation.save()

            sponsorship.current_amount += donation.amount
            sponsorship.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def pet_detail_api(request, pet_id):
    try:
        pet = StrayAnimal.objects.get(id=pet_id)

        # Recently viewed
        recently_viewed = request.session.get('recently_viewed', [])
        if pet.id in recently_viewed:
            recently_viewed.remove(pet.id)
        recently_viewed.insert(0, pet.id)
        request.session['recently_viewed'] = recently_viewed[:10]

        # Medical info
        medical = MedicalSponsorship.objects.filter(pet=pet, is_active=True).first()

        data = {
            "id": pet.id,
            "name": pet.name,
            "pet_id": pet.pet_id,
            "breed": pet.breed,
            "species": pet.species,
            "age": pet.age_value,
            "age_unit": pet.age_unit,
            "gender": pet.gender,
            "size": pet.size,
            "coat_length": pet.coat_length,
            "good_with": pet.good_with,
            "color": pet.color,
            "care_and_behavior": pet.care_and_behavior,
            "days_on_pawpal": pet.days_on_pawpal,
            "location": pet.location,
            "image_url": pet.image.url if pet.image else "",
            "story": pet.story_describe,
            "health_status": pet.health_status,
            "behavior": pet.behavior,

            # Medical section (if exists)
            "sponsorship": {
                "id": medical.id,
                "goal_amount": float(medical.goal_amount),
                "current_amount": float(medical.current_amount),
                "description": medical.description,
                "progress": medical.get_progress_percent()
            } if medical else None
        }

        return JsonResponse(data)

    except StrayAnimal.DoesNotExist:
        return JsonResponse({'error': 'Pet not found'}, status=404)

# Adopt View
def adopt(request):
    query = request.GET.get('q')
    species = request.GET.get('species')
    breed = request.GET.get('breed')
    age_category = request.GET.get('age')  # puppy, young, adult, senior
    size = request.GET.get('size')
    gender = request.GET.get('gender')
    color_raw = request.GET.get('color')
    color = unquote_plus(color_raw) if color_raw else None
    sort = request.GET.get('sort', 'random')

    animals = StrayAnimal.objects.filter(is_adopted=False)

    species_counts = (
        StrayAnimal.objects
        .filter(is_adopted=False)
        .values('species')
        .annotate(count=Count('id'))
    )

    size_counts = (
        StrayAnimal.objects
        .filter(is_adopted=False)
        .values('size')
        .annotate(count=Count('id'))
    )

    gender_counts = (
        StrayAnimal.objects
        .filter(is_adopted=False)
        .values('gender')
        .annotate(count=Count('id'))
    )

    color_counts = (
        StrayAnimal.objects
        .filter(is_adopted=False)
        .values('color')
        .annotate(count=Count('id'))
    )

    if query:
        animals = animals.filter(
            Q(name__icontains=query) |
            Q(breed__icontains=query) |
            Q(pet_id__icontains=query) |
            Q(color__icontains=query)
        )

    if species:
        animals = animals.filter(species=species)
    if breed:
        animals = animals.filter(breed__icontains=breed)
    if size:
        animals = animals.filter(size=size)
    if gender:
        animals = animals.filter(gender=gender)
    if color:
        animals = animals.filter(color=color)
    if age_category:
        def matches_age_category(a):
            return a.get_age_category().lower() == age_category.lower()
        animals = [a for a in animals if matches_age_category(a)]
    

    # ✅ Sorting should be applied only on QuerySet, not list
    if not isinstance(animals, list):
        if sort == 'oldest':
            animals = animals.order_by('created_at')
        elif sort == 'random':
            animals = animals.order_by('?')
        else:
            animals = animals.order_by('-created_at')

    

    # ✅ all_pets exclude filtered pets
    filtered_ids = [a.id for a in animals] if isinstance(animals, list) else animals.values_list('id', flat=True)
    all_pets = StrayAnimal.objects.filter(is_adopted=False).exclude(id__in=filtered_ids)[:12]

    recently_ids = request.session.get('recently_viewed', [])[:5]
    recently_pets = StrayAnimal.objects.filter(id__in=recently_ids)


    context = {
        'available_pets': animals,
        'recently_viewed': recently_pets,
        'filters_applied': any([query, species, breed, size, gender, color, age_category]),
        'query': query,
        'species': species,
        'breed': breed,
        'size': size,
        'gender': gender,
        'color': color,
        'color_choices': [color[0] for color in StrayAnimal.COLOR_CHOICES],
        'age': age_category,
        'age_choices': ['Puppy', 'Young', 'Adult', 'Senior'],
        'sort': sort,
        'all_pets': all_pets,
    }

    context.update({
    'species_counts': {item['species']: item['count'] for item in species_counts},
    'size_counts': {item['size']: item['count'] for item in size_counts},
    'gender_counts': {item['gender']: item['count'] for item in gender_counts},
    'color_counts': {item['color']: item['count'] for item in color_counts},
})
    return render(request, 'adopt.html', context)


def recently_viewed_partial(request):
    recently_ids = request.session.get('recently_viewed', [])[:5]
    recently_pets = StrayAnimal.objects.filter(id__in=recently_ids)
    html = render_to_string('partials/recently_viewed.html', {'recently_viewed': recently_pets})
    return HttpResponse(html)


def adoption_request(request):
    pet_ids = request.GET.get("pets", "")
    pet_ids = pet_ids.split(",") if pet_ids else []
    selected_pets = StrayAnimal.objects.filter(id__in=pet_ids)

    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        form.fields['pets'].required = False  # ✅ ปิด validation ชั่วคราว
        if form.is_valid():
           adoption = form.save(commit=False)
           # 🔐 ผูก user ถ้ามี field user ใน model
           if request.user.is_authenticated:
                adoption.user = request.user
        adoption.save()
        adoption.pets.set(selected_pets)

        # ✅ เพิ่ม Notification
        if request.user.is_authenticated:
            pet_names = ', '.join(pet.name for pet in selected_pets)
            Notification.objects.create(
                user=request.user,
                message=f"You submitted an adoption request for: {pet_names} 🎉"
            )
        return redirect('thank_you')
    
    else:
        form = AdoptionRequestForm()

    adoption_steps = [
        "Initial enquiry",
        "Interview",
        "Home Assessment",
        "Adoption agreement",
        "Travel arrangements"
    ]

    context = {
    'form': form,
    'selected_pets': selected_pets,
    'adoption_steps': adoption_steps, 
    }
    return render(request, 'adoption_request_form.html', context)

def thank_you(request):
    return render(request, 'thank_you.html')

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notes})

def generate_promptpay_qr(request):
    amount = request.GET.get("amount", 0)
    try:
        qr_base64 = generate_promptpay_qr_image_base64(mobile="0874919999", amount=amount)
        return JsonResponse({'qr': qr_base64})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decimal import Decimal
from .models import StrayAnimal, SponsorshipDonation

@csrf_exempt
def sponsor_submit(request):
    if request.method == "POST":
        try:
            pet = StrayAnimal.objects.get(id=request.POST.get("pet_id"))
            amount = Decimal(request.POST.get("amount", 0))
            slip = request.FILES.get("payment_slip")

            SponsorshipDonation.objects.create(
                pet=pet,
                donor_name="Anonymous",
                email="anonymous@example.com",
                amount=amount,
                payment_method="promptpay",
                payment_slip=slip,
                user=request.user if request.user.is_authenticated else None
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import StrayAnimal, PersonalityResult
import random
import json

@csrf_exempt
def save_personality_result(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pet_id = data.get("pet_id")

        if not pet_id:
            return JsonResponse({'error': 'No pet_id provided'}, status=400)

        pet = StrayAnimal.objects.filter(id=pet_id).first()
        if not pet:
            return JsonResponse({'error': 'Pet not found'}, status=404)

        if request.user.is_authenticated:
            PersonalityResult.objects.update_or_create(
                user=request.user,
                defaults={
                    'result_pet': pet,
                    'result_summary': f"You matched with {pet.name}, a lovely {pet.breed}!"
                }
            )
        return JsonResponse({'success': True})
    
def personality_test_view(request):
    return render(request, "personality_test.html")

@csrf_exempt
def personality_match_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            q1 = data.get("q1")
            q2 = data.get("q2")
            q3 = data.get("q3")
            q4 = data.get("q4")
            q5 = data.get("q5")

            if not all([q1, q2, q3, q4, q5]):
                return JsonResponse({'error': 'Incomplete answers'}, status=400)

            # Simple logic
            pet = StrayAnimal.objects.filter(is_adopted=False).order_by('?').first()

            if not pet:
                return JsonResponse({'error': 'No available pets'}, status=404)

            if request.user.is_authenticated:
                PersonalityResult.objects.update_or_create(
                    user=request.user,
                    defaults={
                        'result_pet': pet,
                        'result_summary': f"Matched with {pet.name}, a lovely {pet.breed}!"
                    }
                )

            return JsonResponse({
                "success": True,
                "pet": {
                    "id": pet.id,
                    "name": pet.name,
                    "breed": pet.breed,
                    "gender": pet.gender,
                    "age": f"{pet.age_value} {pet.age_unit}",
                    "description": pet.story_describe[:100] + "...",
                    "image_url": pet.image.url if pet.image else ""
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)