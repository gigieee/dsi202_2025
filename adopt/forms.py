from django import forms
from .models import GeneralDonation, SponsorshipDonation, AdoptionRequest

class GeneralDonationForm(forms.ModelForm):
    class Meta:
        model = GeneralDonation
        fields = ['donor_name', 'email', 'amount', 'message', 'payment_method', 'slip_image']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

class SponsorshipDonationForm(forms.ModelForm):
    class Meta:
        model = SponsorshipDonation
        fields = ['donor_name', 'email', 'amount', 'payment_method']
        widgets = {
            'payment_method': forms.RadioSelect,
            }
        

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        exclude = ['status', 'created_at']  # ไม่ให้ user กรอกเอง
        widgets = {
            'household_info': forms.Textarea(attrs={'rows': 3}),
            'other_pets': forms.Textarea(attrs={'rows': 2}),
            'property_description': forms.Textarea(attrs={'rows': 3}),
            'motivation': forms.Textarea(attrs={'rows': 3}),
        }