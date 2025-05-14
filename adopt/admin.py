from django.contrib import admin
from .models import StrayAnimal, GeneralDonation, MedicalSponsorship, SponsorshipDonation, AdoptionRequest, Blog


@admin.register(StrayAnimal)
class StrayAnimalAdmin(admin.ModelAdmin):
    list_display = ('pet_id', 'name', 'breed', 'species', 'is_adopted')
    ordering = ['pet_id']  # เรียงตาม pet_id จากน้อยไปมาก
    search_fields = ['name', 'breed', 'pet_id']
    list_filter = ['species', 'size', 'gender']

@admin.register(GeneralDonation)
class GeneralDonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'payment_method', 'created_at', 'slip_image')
    search_fields = ('donor_name', 'email')

@admin.register(MedicalSponsorship)
class MedicalSponsorshipAdmin(admin.ModelAdmin):
    list_display = ('pet', 'goal_amount', 'current_amount', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('pet__name',)

@admin.register(SponsorshipDonation)
class SponsorshipDonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'get_pet_name', 'payment_method', 'created_at')
    search_fields = ('donor_name', 'email', 'pet__name')

    def get_pet_name(self, obj):
        return obj.pet.name
    get_pet_name.short_description = 'Pet Name'


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('province', 'created_at')
    readonly_fields = ('created_at',)
    filter_horizontal = ('pets',)  # ให้สามารถเลือกสัตว์หลายตัวได้ง่ายขึ้นในหน้าแก้ไข

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)