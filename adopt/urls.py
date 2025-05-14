from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('adopt/', views.adopt, name='adopt'),
    path('donate/', views.donate, name='donate'),
    path('about/', views.about_us, name='about'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('personality/', views.personality_test_view, name='personality_test'),

    # Pet Detail + Favorite
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pet/<int:pet_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('request-adoption/', views.adoption_request, name='adoption_request'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('api/favorite-pets/', views.get_favorite_pets, name='get_favorite_pets'),


    # Donation routes
    path('donate/general/', views.general_donate_view, name='general_donate'),
    path('donate/sponsor/', views.medical_sponsorship_list, name='sponsorship_list'),
    path('donate/sponsor/<int:sponsorship_id>/', views.medical_sponsorship_detail, name='sponsorship_detail'),



    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
]