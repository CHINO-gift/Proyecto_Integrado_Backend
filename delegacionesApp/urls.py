from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio_delegaciones'),
    path('detalle/<str:nombre>/', views.detalle, name='detalle_delegacion'),
]