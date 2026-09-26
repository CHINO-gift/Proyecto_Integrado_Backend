from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def inicio(request):
    return redirect('/delegaciones/')


urlpatterns = [
    path('', inicio, name='inicio'),

    path('admin/', admin.site.urls),

    path('delegaciones/', include('delegacionesApp.urls')),

    path('funcionarios/', include('funcionariosApp.urls')),
]