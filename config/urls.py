
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.shortcuts import redirect

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from . import views


# =========================================================
# SIGED - PAGINA PRINCIPAL
# =========================================================

def inicio(request):
    if request.user.is_authenticated:
        return redirect("panel_principal")

    return redirect("login")


# =========================================================
# RUTAS DEL PROYECTO SIGED
# =========================================================

urlpatterns = [

    # PAGINA PRINCIPAL
    path(
        "",
        inicio,
        name="inicio"
    ),

    # INICIO DE SESION WEB
    path(
        "acceso/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
            next_page="panel_principal"
        ),
        name="login"
    ),

    # CERRAR SESION
    path(
        "salir/",
        auth_views.LogoutView.as_view(
            next_page="login"
        ),
        name="logout"
    ),

    # RECUPERACION DE CONTRASENA
    path(
        "recuperar-contrasena/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.txt",
            subject_template_name="registration/password_reset_subject.txt"
        ),
        name="password_reset"
    ),

    path(
        "recuperar-contrasena/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "restablecer-contrasena/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "restablecer-contrasena/completado/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),

    # DASHBOARD
    path(
        "panel/",
        views.panel_principal,
        name="panel_principal"
    ),

    # MANTENEDOR DE DELEGACIONES
    path(
        "delegaciones/",
        include("delegacionesApp.urls")
    ),

    # MANTENEDOR DE FUNCIONARIOS
    path(
        "funcionarios/",
        include("funcionariosApp.urls")
    ),

    # GESTION DE USUARIOS Y PERFILES
    path(
        "usuarios/",
        include("usuariosApp.urls")
    ),

    # ADMINISTRACION DJANGO
    path(
        "admin/",
        admin.site.urls
    ),

    # =====================================================
    # EVA 4 - AUTENTICACION JWT
    # =====================================================

    # Obtener Access Token y Refresh Token.
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    # Renovar Access Token.
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    # =====================================================
    # EVA 4 - SWAGGER / OPENAPI
    # =====================================================

    # Esquema OpenAPI.
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),

    # Documentacion interactiva Swagger UI.
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui"
    ),

    # Documentacion alternativa ReDoc.
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc"
    ),

]
