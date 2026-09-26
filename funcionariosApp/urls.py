from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio_funcionarios'),
    path('detalle/<int:id>/', views.detalle, name='detalle_funcionario'),
]