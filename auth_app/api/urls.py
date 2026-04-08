from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<str:user_id>/', ProfileView.as_view(), name='profile'),
    path('profiles/business/', ProfileView.as_view(), name='business_profiles'),
    path('profiles/customer/', ProfileView.as_view(), name='customer_profiles'),
]
