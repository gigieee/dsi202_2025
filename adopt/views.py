from django.shortcuts import render, redirect, get_object_or_404
from .models import StrayAnimal, GeneralDonation, MedicalSponsorship, AdoptionRequest, Blog
from .forms import GeneralDonationForm, SponsorshipDonationForm, AdoptionRequestForm
from django.http import JsonResponse
from django.db.models import Sum
import json

def pet_detail(request, pet_id):
    pet = get_object_or_404(StrayAnimal, id=pet_id)

    # ดึง MedicalSponsorship ถ้ามี
    try:
        sponsorship = MedicalSponsorship.objects.get(pet=pet)
    except MedicalSponsorship.DoesNotExist:
        sponsorship = None

    context = {
        'pet': pet,
        'sponsorship': sponsorship
    }
    return render(request, 'pet_detail.html', context)

def toggle_favorite(request, pet_id):
    favorites = request.session.get('favorites', [])
    if pet_id in favorites:
        favorites.remove(pet_id)
    else:
        favorites.append(pet_id)
    request.session['favorites'] = favorites
    return redirect('pet_detail', pet_id=pet_id)

def homepage(request):
    # สัตว์ที่ยังไม่ถูกรับเลี้ยง
    animals = StrayAnimal.objects.filter(is_adopted=False)
    featured = animals[:3]
    total = animals.count()
    remaining = total - len(featured)

    # เอา id ของสัตว์ที่มี medical support
    medical_pet_ids = MedicalSponsorship.objects.values_list('pet_id', flat=True)

    # สำหรับ Section: Animals Needing Medical Help
    sponsored_animals = StrayAnimal.objects.filter(
        is_adopted=False, id__in=medical_pet_ids
    )

    # สำหรับ Section: Support Care for Our PawFriends (exclude medical pet)
    support_animals = StrayAnimal.objects.filter(
        is_adopted=False
    ).exclude(id__in=medical_pet_ids)[:8]

    return render(request, 'homepage.html', {
        'featured_animals': featured,
        'remaining_animals': remaining,
        'sponsored_animals': sponsored_animals,
        'support_animals': support_animals,
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
    ids = request.GET.getlist('ids[]')  # รับ array id
    pets = StrayAnimal.objects.filter(id__in=ids)
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

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def personality_test_view(request):
    return render(request, 'personality_test.html')


#หน้า Overview Donate
def general_donate_view(request):
    if request.method == 'POST':
        form = GeneralDonationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'thank_you.html')
    else:
        form = GeneralDonationForm()
    return render(request, 'donate_general.html', {'form': form})

# หน้าแสดงรายการ sponsorship
def medical_sponsorship_list(request):
    sponsorships = MedicalSponsorship.objects.filter(is_active=True)
    return render(request, 'sponsorship_list.html', {'sponsorships': sponsorships})

# หน้ารายละเอียดและแบบฟอร์มบริจาคเฉพาะสัตว์
def medical_sponsorship_detail(request, sponsorship_id):
    sponsorship = get_object_or_404(MedicalSponsorship, id=sponsorship_id)

    if request.method == 'POST':
        form = SponsorshipDonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.sponsorship = sponsorship
            donation.save()
            return render(request, 'thank_you.html')
    else:
        form = SponsorshipDonationForm()

    return render(request, 'sponsorship_detail.html', {
        'sponsorship': sponsorship,
        'form': form
    })

    
from django.http import JsonResponse



from django.db.models import Q

def adopt(request):
    query = request.GET.get('q')
    filter_species = request.GET.get('species')
    animals = StrayAnimal.objects.filter(is_adopted=False)

    if query:
        animals = animals.filter(
            Q(name__icontains=query) |
            Q(breed__icontains=query) |
            Q(pet_id__icontains=query) |
            Q(color__icontains=query)
        )

    if filter_species:
        animals = animals.filter(species=filter_species)

    context = {
        'available_pets': animals
    }
    return render(request, 'adopt.html', context)


def adoption_request(request):
    pet_ids = request.GET.get("pets", "")
    pet_ids = pet_ids.split(",") if pet_ids else []
    selected_pets = StrayAnimal.objects.filter(id__in=pet_ids)

    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption = form.save()
            adoption.pets.set(selected_pets)  # บันทึก ManyToMany
            adoption.save()
            print("Form submitted")
            return redirect('thank_you')
    else:
        form = AdoptionRequestForm()

    return render(request, 'adoption_request_form.html', {
        'form': form,
        'selected_pets': selected_pets
    })

def thank_you(request):
    return render(request, 'thank_you.html')

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

