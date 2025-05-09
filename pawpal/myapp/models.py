from django.db import models
class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'เพศผู้'), ('Female', 'เพศเมีย')])
    description = models.TextField(blank=True)
    health_issues = models.TextField(blank=True)
    vaccination = models.TextField(blank=True)
    personality = models.TextField(blank=True)
    special_needs = models.TextField(blank=True)

    def __str__(self):
        return self.name

class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pets/images/')