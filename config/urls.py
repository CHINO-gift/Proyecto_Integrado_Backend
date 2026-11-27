
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

    # =====================================================
    # EVA 3 - PAGINA PRINCIPAL
    # =====================================================

    path(
        "",
        inicio,
        name="inicio"
    ),

    # =====================================================
    # EVA 3 - INICIO DE SESION
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
    # EVA 3 - CERRAR SESION
    # =====================================================

    path(
        "salir/",
        auth_views.LogoutView.as_view(
            next_page="login"
        ),
        name="logout"
    ),

    # =====================================================
    # EVA 3 - RECUPERACION DE CONTRASENA
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

    # =====================================================
    # EVA 3 - DASHBOARD
    # =====================================================

    path(
        "panel/",
        views.panel_principal,
        name="panel_principal"
    ),

    # =====================================================
    # EVA 3 - MANTENEDOR WEB DE DELEGACIONES
    # =====================================================

    path(
        "delegaciones/",
        include("delegacionesApp.urls")
    ),

    # =====================================================
    # EVA 3 - MANTENEDOR WEB DE FUNCIONARIOS
    # =====================================================

    path(
        "funcionarios/",
        include("funcionariosApp.urls")
    ),

    # =====================================================
    # EVA 3 - GESTION DE USUARIOS
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

    # =====================================================
    # EVA 4 - API RESTFUL DE DELEGACIONES
    # =====================================================

    path(
        "api/delegaciones/",
        include("delegacionesApp.api_urls")
    ),

    # =====================================================
    # EVA 4 - AUTENTICACION JWT
    # =====================================================

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    # =====================================================
    # EVA 4 - SWAGGER / OPENAPI
    # =====================================================

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),

    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui"
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc"
    ),

]
