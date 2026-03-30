from django.urls import path
from .views import RegisterView, LoginView, ProfileCheckView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:user_id>/', ProfileCheckView.as_view(), name='profile'),
    path('profiles/business/', ProfileCheckView.as_view(), name='business_profiles'),
    path('profiles/customer/', ProfileCheckView.as_view(), name='customer_profiles'),
]
