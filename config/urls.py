
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.shortcuts import redirect

from . import views


# ==========================================
# EVA 3 - PÁGINA PRINCIPAL
# ==========================================

def inicio(request):

    # Si ya inició sesión, abrir SIGED
    if request.user.is_authenticated:
        return redirect('panel_principal')

    # Si no ha iniciado sesión, mostrar login
    return redirect('login')


# ==========================================
# RUTAS PRINCIPALES DE SIGED
# ==========================================

urlpatterns = [

    # ======================================
    # INICIO
    # ======================================

    path(
        '',
        inicio,
        name='inicio'
    ),


    # ======================================
    # EVA 3 - INICIO DE SESIÓN
    # ======================================

    path(
        'acceso/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            redirect_authenticated_user=True,
            next_page='panel_principal'
        ),
        name='login'
    ),


    # ======================================
    # EVA 3 - CERRAR SESIÓN
    # ======================================

    path(
        'salir/',
        auth_views.LogoutView.as_view(
            next_page='login'
        ),
        name='logout'
    ),


    # ======================================
    # EVA 3 - DASHBOARD DE SIGED
    # ======================================

    path(
        'panel/',
        views.panel_principal,
        name='panel_principal'
    ),


    # ======================================
    # EVA 2 - DELEGACIONES
    # ======================================

    path(
        'delegaciones/',
        include('delegacionesApp.urls')
    ),


    # ======================================
    # EVA 2 - FUNCIONARIOS
    # ======================================

    path(
        'funcionarios/',
        include('funcionariosApp.urls')
    ),


    # ======================================
    # ADMINISTRACIÓN DJANGO
    # ======================================

    path(
        'admin/',
        admin.site.urls
    ),

]
