from django.db import models
from multiselectfield import MultiSelectField

# Create models here
class Animal(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
    ]
    
    
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    breed = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='animal_images/', null=True, blank=True)
    is_adopted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.species})"
    
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
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='animal_images/', blank=True, null=True)
    story = models.TextField()
    behavior = models.CharField(max_length=50, choices=BEHAVIOR_CHOICES)
    health_status = models.TextField()
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