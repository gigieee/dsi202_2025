from django.contrib import admin
from django.utils.html import format_html
from .models import StrayAnimal, GeneralDonation, MedicalSponsorship, SponsorshipDonation, AdoptionRequest, Blog, MedicalDonation
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

# ✅ Register again using your custom admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_active', 'last_login', 'date_joined']

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

@admin.register(MedicalDonation)
class MedicalDonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'email', 'amount', 'created_at', 'slip_image_tag']
    readonly_fields = ['slip_image_tag']
    search_fields = ['donor_name', 'email']
    list_filter = ['created_at']

    def slip_image_tag(self, obj):
        if obj.slip_image:
            return format_html('<img src="{}" style="max-width:300px;" />', obj.slip_image.url)
        return "-"
    slip_image_tag.short_description = "Slip Preview"


@admin.register(SponsorshipDonation)
class SponsorshipDonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'email', 'pet', 'amount', 'payment_method', 'created_at')
    readonly_fields = ('preview_slip',)
    fields = ('donor_name', 'email', 'pet', 'amount', 'payment_method', 'payment_slip', 'preview_slip', 'created_at')

    def preview_slip(self, obj):
        if obj.payment_slip:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.payment_slip.url)
        return "No Slip Uploaded"
    preview_slip.short_description = "Slip Preview"