from django.urls import path
from . import views
from .views import pet_detail_api, generate_promptpay_qr, medical_sponsorship_detail, medical_donate, sponsor_submit, user_dashboard, custom_logout_view
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    next_page = reverse_lazy('homepage') 

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    

    path('adopt/', views.adopt, name='adopt'),
    path('adopt/recently-viewed-html/', views.recently_viewed_partial, name='recently_viewed_partial'),
    path('donate/', views.donate, name='donate'),
    path('about/', views.about_us, name='about'),

    # Pet Detail + Favorite
    path('pet/<int:pet_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('api/favorite-pets/', views.get_favorite_pets, name='get_favorite_pets'),
    path('api/pet/<int:pet_id>/', views.pet_detail_api, name='pet_detail_api'),
    path('favorites/', views.favorites_view, name='favorites'),

    # Donation routes
    path('donate/general/', views.general_donate, name='general_donate'),
    path('donate/sponsor/', views.medical_sponsorship_list, name='sponsorship_list'),
    path('donate/sponsor/<int:sponsorship_id>/', medical_sponsorship_detail, name='sponsorship_detail'),
    path('donate/medical/<int:sponsorship_id>/', views.medical_donate, name='medical_donate'),
    path('donate/sponsor-submit/', views.sponsor_submit, name='sponsor_submit'),
   # others 
    path('request-adoption/', views.adoption_request, name='adoption_request'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('notifications/', views.notifications, name='notifications'),

    path('generate-promptpay-qr/', generate_promptpay_qr, name='generate_promptpay_qr'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('logout/', custom_logout_view, name='logout'),
    
    path("api/track-recently-viewed/<int:pet_id>/", views.add_recently_viewed, name="track_recently_viewed"),

    path("personality/save_result/", views.save_personality_result, name="save_personality_result"),
    path("personality/", views.personality_test_view, name="personality_test"),
    path("api/personality-match/", views.personality_match_api, name="personality_match_api"),
]