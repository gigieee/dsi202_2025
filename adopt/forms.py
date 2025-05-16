from django import forms
from .models import GeneralDonation, SponsorshipDonation, AdoptionRequest, MedicalDonation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

class MedicalDonationForm(forms.ModelForm):
    class Meta:
        model = MedicalDonation
        fields = ['donor_name', 'email', 'amount', 'slip_image']
        

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

class CustomSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hash password
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)