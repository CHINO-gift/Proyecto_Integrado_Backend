
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.shortcuts import redirect

from . import views


# =========================================================
# SIGED EVA 3 - PAGINA PRINCIPAL
# =========================================================

def inicio(request):

    # Si el usuario ya inicio sesion,
    # redirigir al panel correspondiente.

    if request.user.is_authenticated:
        return redirect("panel_principal")

    # Si no ha iniciado sesion, mostrar login.

    return redirect("login")


# =========================================================
# SIGED EVA 3 - RUTAS PRINCIPALES
# =========================================================

urlpatterns = [

    # =====================================================
    # PAGINA PRINCIPAL
    # =====================================================

    path(
        "",
        inicio,
        name="inicio"
    ),

    # =====================================================
    # INICIO DE SESION
    # =====================================================

    path(
        "acceso/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
            next_page="panel_principal"
        ),
        name="login"
    ),

    # =====================================================
    # CERRAR SESION
    # =====================================================

    path(
        "salir/",
        auth_views.LogoutView.as_view(
            next_page="login"
        ),
        name="logout"
    ),

    # =====================================================
    # RECUPERACION DE CONTRASENA - SOLICITUD
    # =====================================================

    path(
        "recuperar-contrasena/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.txt",
            subject_template_name="registration/password_reset_subject.txt"
        ),
        name="password_reset"
    ),

    # =====================================================
    # RECUPERACION - SOLICITUD PROCESADA
    # =====================================================

    path(
        "recuperar-contrasena/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    # =====================================================
    # RECUPERACION - NUEVA CONTRASENA
    # =====================================================

    path(
        "restablecer-contrasena/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    # =====================================================
    # RECUPERACION - PROCESO COMPLETADO
    # =====================================================

    path(
        "restablecer-contrasena/completado/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),

    # =====================================================
    # DASHBOARD PRINCIPAL
    # =====================================================

    path(
        "panel/",
        views.panel_principal,
        name="panel_principal"
    ),

    # =====================================================
    # GESTION DE DELEGACIONES
    # =====================================================

    path(
        "delegaciones/",
        include("delegacionesApp.urls")
    ),

    # =====================================================
    # GESTION DE FUNCIONARIOS
    # =====================================================

    path(
        "funcionarios/",
        include("funcionariosApp.urls")
    ),

    # =====================================================
    # EVA 3 - GESTION DE USUARIOS Y PERFILES
    # =====================================================

    path(
        "usuarios/",
        include("usuariosApp.urls")
    ),

    # =====================================================
    # ADMINISTRACION DJANGO
    # =====================================================

    path(
        "admin/",
        admin.site.urls
    ),

]
