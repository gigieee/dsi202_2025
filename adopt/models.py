from django.db import models

# Create your models here.
class Animal(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
    ]
    
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    breed = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='animal_images/', null=True, blank=True)
    is_adopted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.species})"