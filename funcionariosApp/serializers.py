
from rest_framework import serializers

from delegacionesApp.models import Delegacion
from .models import Funcionario


# =========================================================
# SIGED EVA 4 - SERIALIZER DE FUNCIONARIOS
# =========================================================

class FuncionarioSerializer(serializers.ModelSerializer):
    """
    Serializador del mantenedor API RESTful de Funcionarios.

    Permite:
    - Convertir funcionarios a formato JSON.
    - Validar datos recibidos mediante POST, PUT y PATCH.
    - Comprobar la existencia de la delegacion asignada.
    - Impedir valores negativos en meta y avance.
    - Impedir que el avance supere la meta.
    - Mostrar porcentaje y estado como campos calculados.
    """

    delegacion = serializers.PrimaryKeyRelatedField(
        queryset=Delegacion.objects.all()
    )

    porcentaje = serializers.IntegerField(
        read_only=True
    )

    estado = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Funcionario

        fields = [
            "id",
            "nombre",
            "cargo",
            "delegacion",
            "meta",
            "avance",
            "porcentaje",
            "estado",
        ]

        read_only_fields = [
            "id",
            "porcentaje",
            "estado",
        ]

        extra_kwargs = {
            "nombre": {
                "required": True,
                "allow_blank": False,
                "trim_whitespace": True,
                "max_length": 100,
            },
            "cargo": {
                "required": True,
                "allow_blank": False,
                "trim_whitespace": True,
                "max_length": 100,
            },
            "meta": {
                "required": False,
                "min_value": 0,
            },
            "avance": {
                "required": False,
                "min_value": 0,
            },
        }

    # =====================================================
    # VALIDAR NOMBRE
    # =====================================================

    def validate_nombre(self, value):
        nombre = value.strip()

        if not nombre:
            raise serializers.ValidationError(
                "Debe ingresar el nombre del funcionario."
            )

        return nombre

    # =====================================================
    # VALIDAR CARGO
    # =====================================================

    def validate_cargo(self, value):
        cargo = value.strip()

        if not cargo:
            raise serializers.ValidationError(
                "Debe ingresar el cargo del funcionario."
            )

        return cargo

    # =====================================================
    # VALIDAR META Y AVANCE
    # =====================================================

    def validate(self, attrs):
        """
        Valida los valores efectivos considerando tambien
        los datos existentes del funcionario.

        Esto permite comprobar correctamente las
        modificaciones parciales realizadas mediante PATCH.
        """

        instancia = self.instance

        meta = attrs.get(
            "meta",
            instancia.meta if instancia is not None else 0
        )

        avance = attrs.get(
            "avance",
            instancia.avance if instancia is not None else 0
        )

        if meta < 0:
            raise serializers.ValidationError({
                "meta": "La meta no puede ser negativa."
            })

        if avance < 0:
            raise serializers.ValidationError({
                "avance": "El avance no puede ser negativo."
            })

        if avance > meta:
            raise serializers.ValidationError({
                "avance": (
                    "El avance no puede superar "
                    "la meta asignada."
                )
            })

        return attrs
