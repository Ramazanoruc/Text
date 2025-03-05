from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Ana sayfa
    path('predict/', views.predict, name='predict'),  # Tahmin işlemi
]