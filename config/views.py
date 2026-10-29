
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from delegacionesApp.models import Delegacion
from funcionariosApp.models import Funcionario


# ==========================================
# EVA 3 - PERFILES DE USUARIO
# ==========================================

def obtener_perfil(usuario):

    # Los superusuarios tienen acceso
    # como Administrador.

    if usuario.is_superuser:
        return "Administrador"

    # Comprobar los grupos del usuario.

    perfiles = [
        "Administrador",
        "Supervisor",
        "Administrativo"
    ]

    for perfil in perfiles:

        if usuario.groups.filter(
            name=perfil
        ).exists():

            return perfil

    # Usuario sin perfil asignado.

    return None


# ==========================================
# EVA 3 - DASHBOARD PRINCIPAL
# ==========================================

@login_required(login_url="login")
def panel_principal(request):

    usuario = request.user

    # Identificar el perfil del usuario.

    perfil = obtener_perfil(usuario)

    # Impedir el acceso a usuarios
    # que no tienen un perfil válido.

    if perfil is None:
        raise PermissionDenied(
            "No tienes un perfil asignado en SIGED."
        )

    # Consultar información del sistema.

    total_delegaciones = Delegacion.objects.count()

    total_funcionarios = Funcionario.objects.count()

    # Preparar los datos del dashboard.

    contexto = {
        "perfil": perfil,
        "total_delegaciones": total_delegaciones,
        "total_funcionarios": total_funcionarios,

        "es_administrador": perfil == "Administrador",
        "es_supervisor": perfil == "Supervisor",
        "es_administrativo": perfil == "Administrativo",
    }

    return render(
        request,
        "panel/inicio.html",
        contexto
    )
