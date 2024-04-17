from django.urls import path
from . import views

urlpatterns = [
    # Existing URL patterns
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
]