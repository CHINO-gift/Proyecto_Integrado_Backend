
from functools import wraps

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied

from django.db import transaction
from django.db.models import Q

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.views.decorators.http import require_http_methods

from .forms import (
    UsuarioCreacionForm,
    UsuarioEdicionForm,
    PERFILES_SIGED,
)


# =========================================================
# SIGED EVA 3 - GESTION DE USUARIOS Y PERFILES
# =========================================================

User = get_user_model()


# =========================================================
# VERIFICAR PERMISOS DE ADMINISTRADOR
# =========================================================

def solo_administrador(vista):

    @wraps(vista)
    def verificar_permiso(request, *args, **kwargs):

        usuario = request.user

        # Verificar que el usuario tenga una cuenta activa.

        if not usuario.is_authenticated or not usuario.is_active:

            raise PermissionDenied(
                "Debes iniciar sesión con una cuenta activa."
            )

        # Los superusuarios tienen acceso administrativo.

        if usuario.is_superuser:
            return vista(request, *args, **kwargs)

        # Comprobar pertenencia al grupo Administrador.

        es_administrador = usuario.groups.filter(
            name="Administrador"
        ).exists()

        if not es_administrador:

            raise PermissionDenied(
                "No tienes permisos para gestionar usuarios."
            )

        return vista(request, *args, **kwargs)

    return verificar_permiso


# =========================================================
# ASIGNAR PERFIL DE SIGED
# =========================================================

def asignar_perfil(usuario, perfil):

    # Quitar únicamente los perfiles anteriores de SIGED.
    # Se conservan otros grupos que pudieran existir.

    grupos_anteriores = list(
        usuario.groups.filter(
            name__in=PERFILES_SIGED
        )
    )

    if grupos_anteriores:
        usuario.groups.remove(*grupos_anteriores)

    # Asignar el perfil seleccionado.

    usuario.groups.add(perfil)


# =========================================================
# LISTAR Y BUSCAR USUARIOS
# =========================================================

@login_required(login_url="login")
@solo_administrador
def inicio(request):

    busqueda = request.GET.get("q", "").strip()

    usuarios = User.objects.prefetch_related(
        "groups"
    ).order_by("username")

    # Buscar por usuario, nombre, apellido o correo.

    if busqueda:

        usuarios = usuarios.filter(
            Q(username__icontains=busqueda)
            | Q(first_name__icontains=busqueda)
            | Q(last_name__icontains=busqueda)
            | Q(email__icontains=busqueda)
        )

    contexto = {
        "usuarios": usuarios,
        "busqueda": busqueda,
        "total_usuarios": usuarios.count(),
    }

    return render(
        request,
        "usuarios/inicio.html",
        contexto
    )


# =========================================================
# CREAR USUARIO
# =========================================================

@login_required(login_url="login")
@solo_administrador
@require_http_methods(["GET", "POST"])
def crear_usuario(request):

    if request.method == "POST":

        formulario = UsuarioCreacionForm(
            request.POST
        )

        if formulario.is_valid():

            with transaction.atomic():

                # UserCreationForm cifra la contraseña
                # antes de guardar el usuario.

                usuario = formulario.save(
                    commit=False
                )

                # Las cuentas nuevas deben ser usuarios
                # normales, no superusuarios de Django.

                usuario.is_active = True
                usuario.is_staff = False
                usuario.is_superuser = False

                usuario.save()

                # Asignar el perfil de SIGED.

                perfil = formulario.cleaned_data[
                    "perfil"
                ]

                asignar_perfil(
                    usuario,
                    perfil
                )

            messages.success(
                request,
                f"El usuario {usuario.username} "
                "fue registrado correctamente."
            )

            return redirect(
                "inicio_usuarios"
            )

    else:

        formulario = UsuarioCreacionForm()

    contexto = {
        "formulario": formulario,
        "titulo": "Agregar usuario",
        "accion": "Guardar usuario",
        "es_creacion": True,
    }

    return render(
        request,
        "usuarios/formulario.html",
        contexto
    )


# =========================================================
# MODIFICAR USUARIO
# =========================================================

@login_required(login_url="login")
@solo_administrador
@require_http_methods(["GET", "POST"])
def editar_usuario(request, id):

    usuario = get_object_or_404(
        User,
        pk=id
    )

    # Impedir modificaciones a superusuarios.

    if usuario.is_superuser:

        raise PermissionDenied(
            "Las cuentas de superusuario están protegidas."
        )

    # Impedir que un administrador altere
    # accidentalmente su propia cuenta.

    if usuario.pk == request.user.pk:

        raise PermissionDenied(
            "No puedes modificar tu propia cuenta "
            "desde este módulo."
        )

    if request.method == "POST":

        formulario = UsuarioEdicionForm(
            request.POST,
            instance=usuario
        )

        if formulario.is_valid():

            with transaction.atomic():

                usuario = formulario.save()

                # Actualizar el perfil del usuario.

                perfil = formulario.cleaned_data[
                    "perfil"
                ]

                asignar_perfil(
                    usuario,
                    perfil
                )

            messages.success(
                request,
                f"Los datos de {usuario.username} "
                "fueron actualizados correctamente."
            )

            return redirect(
                "inicio_usuarios"
            )

    else:

        formulario = UsuarioEdicionForm(
            instance=usuario
        )

    contexto = {
        "formulario": formulario,
        "usuario_editado": usuario,
        "titulo": "Modificar usuario",
        "accion": "Guardar cambios",
        "es_creacion": False,
    }

    return render(
        request,
        "usuarios/formulario.html",
        contexto
    )
