
import os
import django

# ==========================================
# CONFIGURAR ENTORNO DJANGO
# ==========================================

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from delegacionesApp.models import Delegacion
from funcionariosApp.models import Funcionario


# ==========================================
# EVA 3 - PERFILES Y PERMISOS
# ==========================================

PERFILES = {
    "Administrador": [
        "view",
        "add",
        "change",
        "delete",
    ],

    "Supervisor": [
        "view",
        "add",
        "change",
    ],

    "Administrativo": [
        "view",
    ],
}


# ==========================================
# MODELOS A ADMINISTRAR
# ==========================================

MODELOS = [
    Delegacion,
    Funcionario,
]


# ==========================================
# CONFIGURAR PERMISOS
# ==========================================

@transaction.atomic
def configurar_permisos():

    print("\nCONFIGURANDO PERMISOS DE SIGED")
    print("=" * 45)

    tipos = [
        ContentType.objects.get_for_model(modelo)
        for modelo in MODELOS
    ]

    for nombre_perfil, acciones in PERFILES.items():

        grupo, creado = Group.objects.get_or_create(
            name=nombre_perfil
        )

        permisos_nuevos = []

        for modelo, tipo in zip(MODELOS, tipos):

            for accion in acciones:

                codigo = (
                    f"{accion}_{modelo._meta.model_name}"
                )

                permiso = Permission.objects.get(
                    content_type=tipo,
                    codename=codigo
                )

                permisos_nuevos.append(permiso)

        # Retirar permisos anteriores solamente
        # de los dos modelos que configuramos.

        permisos_anteriores = list(
            grupo.permissions.filter(
                content_type__in=tipos
            )
        )

        if permisos_anteriores:
            grupo.permissions.remove(
                *permisos_anteriores
            )

        # Asignar permisos según el perfil.

        grupo.permissions.add(
            *permisos_nuevos
        )

        print(f"\nPerfil: {nombre_perfil}")
        print(f"Permisos asignados: {len(permisos_nuevos)}")

        for permiso in permisos_nuevos:
            print(f" - {permiso.codename}")

    print("\n" + "=" * 45)
    print("PERMISOS CONFIGURADOS CORRECTAMENTE")


# ==========================================
# EJECUCIÓN
# ==========================================

if __name__ == "__main__":
    configurar_permisos()
