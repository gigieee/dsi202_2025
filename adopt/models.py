from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User

#Stray Animals
class StrayAnimal(models.Model):
    # --- Choices ---
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
    ]

    AGE_UNIT_CHOICES = [
        ('day', 'Day(s)'),
        ('week', 'Week(s)'),
        ('month', 'Month(s)'),
        ('year', 'Year(s)'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('extra large', 'Extra Large')
    ]

    COAT_LENGTH_CHOICES = [
        ('hairless', 'Hairless'),
        ('short', 'Short'),
        ('medium', 'Medium'),
        ('long', 'Long'),
        ('wire', 'Wire'),
        ('curly', 'Curly')
    ]

    GOOD_WITH_CHOICES = [
        ('kids', 'Kids'),
        ('other dogs', 'Other Dogs'),
        ('cats', 'Cats')
    ]

    COLOR_CHOICES = [
        ('Apricot / Beige', 'Apricot / Beige'),
        ('Bicolor', 'Bicolor'),
        ('Black', 'Black'),
        ('Brindle', 'Brindle'),
        ('Brown/Chocolate', 'Brown/Chocolate'),
        ('Golden', 'Golden'),
        ('Gray/Blue/Silver', 'Gray/Blue/Silver'),
        ('Harlequin', 'Harlequin'),
        ('Merle (Blue)', 'Merle (Blue)'),
        ('Merle (Red)', 'Merle (Red)'),
        ('Red / Chestnut / Orange', 'Red / Chestnut / Orange'),
        ('Sable', 'Sable'),
        ('Tricolor (Brown,Black, & White)', 'Tricolor (Brown,Black, & White)'),
        ('White / Cream', 'White / Cream'),
        ('Yellow / Tan / Blond / Fawn', 'Yellow / Tan / Blond / Fawn'),
    ]

    CARE_CHOICES = [
        ('House-trained', 'House-trained'),
        ('Special Needs', 'Special Needs'),
    ]

    BEHAVIOR_CHOICES = [
        ('Anxiety', 'Anxiety'),
        ('Barking and Howling', 'Barking and Howling'),
        ('Biting', 'Biting'),
        ('Chewing', 'Chewing'),
        ('Others', 'Others')
    ]

    DAYS_ON_PAWPAL_CHOICES = [
        ('Any', 'Any'),
        ('1', '1'),
        ('7', '7'),
        ('14', '14'),
        ('30+', '30+'),
    ]

    pet_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    age_value = models.PositiveIntegerField()
    age_unit = models.CharField(max_length=10, choices=AGE_UNIT_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    coat_length = models.CharField(max_length=20, choices=COAT_LENGTH_CHOICES)
    good_with = MultiSelectField(
        choices=GOOD_WITH_CHOICES,
        blank=True,
        max_length=50,
        verbose_name="Good with"
    )
    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    care_and_behavior = models.CharField(max_length=50, choices=CARE_CHOICES)
    days_on_pawpal = models.CharField(max_length=10, choices=DAYS_ON_PAWPAL_CHOICES)
    location = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='animal_images/', blank=True, null=True)
    story_describe = models.TextField(blank=True)
    behavior = models.CharField(max_length=50, choices=BEHAVIOR_CHOICES)
    health_status = models.TextField(blank=True)
    is_adopted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_age_in_years(self):
        if self.age_unit == 'day':
            return self.age_value / 365
        elif self.age_unit == 'week':
            return self.age_value / 52
        elif self.age_unit == 'month':
            return self.age_value / 12
        return self.age_value

    def get_age_category(self):
        age = self.get_age_in_years()
        if age < 1:
            return "Puppy"
        elif age < 3:
            return "Young"
        elif age < 8:
            return "Adult"
        else:
            return "Senior"
        
    def save(self, *args, **kwargs):
        if not self.pet_id:
            prefix = 'D' if self.species == 'Dog' else 'C'
            count = StrayAnimal.objects.filter(species=self.species).count() + 1
            self.pet_id = f"{prefix}{count:03d}"  # D001, C002
        super(StrayAnimal, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.breed} ({self.pet_id})"


#Donation & Supporting 
# Overview Donate - ไม่อิงสัตว์รายตัว
class GeneralDonation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    donor_name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('promptpay', 'PromptPay'),
        ('credit_card', 'Credit Card'),
    ])
    slip_image = models.ImageField(upload_to='donation_slips/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount} THB"


# Medical Sponsorship - สำหรับกรณีบริจาคเพื่อการรักษาสัตว์
class MedicalSponsorship(models.Model):
    
    pet = models.ForeignKey("adopt.StrayAnimal", on_delete=models.CASCADE, related_name="medical_support")
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(help_text="Explain the medical condition or need")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} Medical Fund"

    def get_progress_percent(self):
        if self.goal_amount == 0:
            return 0
        return min(round((self.current_amount / self.goal_amount) * 100, 2), 100)

class MedicalDonation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sponsorship = models.ForeignKey(MedicalSponsorship, on_delete=models.CASCADE, related_name='donations')
    donor_name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    slip_image = models.ImageField(upload_to='medical_donation_slips/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} -> {self.sponsorship.pet.name} ({self.amount} THB)"


# Record of donation under sponsorship
class SponsorshipDonation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pet = models.ForeignKey(
    StrayAnimal, 
    on_delete=models.CASCADE,
    null=True,  # ชั่วคราว
    blank=True  # เผื่อในฟอร์ม admin
)
    donor_name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
    max_length=50,
    choices=[
        ('promptpay', 'PromptPay'),
        ('credit_card', 'Credit Card'),
    ]
)
    payment_slip = models.ImageField(upload_to='sponsorship_slips/', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} -> {self.pet.name} ({self.amount} THB)"

# Adoption
class AdoptionRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pets = models.ManyToManyField(StrayAnimal, related_name='adoption_requests')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    subdistrict = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    household_info = models.TextField()
    other_pets = models.TextField(blank=True)
    property_description = models.TextField()
    jobs = models.CharField(max_length=200, default='Not specified')
    motivation = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog/')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.user.username} – {self.message[:40]}"
    

class FavoritePet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey('StrayAnimal', on_delete=models.CASCADE)

class RecentlyViewedPet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey('StrayAnimal', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

class PersonalityResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    result_pet = models.ForeignKey(StrayAnimal, on_delete=models.SET_NULL, null=True)
    result_summary = models.TextField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
