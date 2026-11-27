
from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Delegacion
from funcionariosApp.models import Funcionario


# =========================================================
# SIGED EVA 4 - DATOS DEL FUNCIONARIO INICIAL
# =========================================================

class FuncionarioInicialAPISerializer(serializers.Serializer):
    """
    Valida los datos del funcionario que se registrara
    junto con una nueva delegacion.

    El campo delegacion no se solicita porque su
    relacion se establece automaticamente.
    """

    nombre = serializers.CharField(
        max_length=100,
        allow_blank=False,
        trim_whitespace=True
    )

    cargo = serializers.CharField(
        max_length=100,
        allow_blank=False,
        trim_whitespace=True
    )

    meta = serializers.IntegerField(
        min_value=0,
        default=0
    )

    avance = serializers.IntegerField(
        min_value=0,
        default=0
    )

    def validate(self, attrs):
        meta = attrs.get("meta", 0)
        avance = attrs.get("avance", 0)

        if avance > meta:
            raise serializers.ValidationError({
                "avance": (
                    "El avance no puede superar "
                    "la meta asignada."
                )
            })

        return attrs


# =========================================================
# SIGED EVA 4 - TRANSACCION DE REGISTRO CONJUNTO
# =========================================================

class RegistroConjuntoSerializer(serializers.Serializer):
    """
    Permite registrar una delegacion y un funcionario
    inicial mediante una sola solicitud JSON.

    Ambas entidades se guardan dentro de una
    transaccion atomica.

    Si ocurre un error durante el registro del
    funcionario, Django revierte tambien la creacion
    de la delegacion.
    """

    nombre = serializers.CharField(
        max_length=100,
        allow_blank=False,
        trim_whitespace=True,
        validators=[
            UniqueValidator(
                queryset=Delegacion.objects.all(),
                message=(
                    "Ya existe una delegación con ese nombre."
                )
            )
        ]
    )

    sector = serializers.CharField(
        max_length=150,
        allow_blank=False,
        trim_whitespace=True
    )

    descripcion = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True
    )

    funcionario = FuncionarioInicialAPISerializer()

    # =====================================================
    # CREAR AMBAS ENTIDADES
    # =====================================================

    def create(self, validated_data):
        """
        Registra las dos entidades en una sola operacion.

        La transaccion se confirma solamente cuando
        ambas operaciones terminan correctamente.
        """

        datos_funcionario = validated_data.pop(
            "funcionario"
        )

        with transaction.atomic():

            # 1. Crear delegacion.
            delegacion = Delegacion.objects.create(
                **validated_data
            )

            # 2. Crear funcionario inicial.
            funcionario = Funcionario.objects.create(
                delegacion=delegacion,
                **datos_funcionario
            )

        # La vista API utilizara estos objetos para
        # construir la respuesta JSON.
        return {
            "delegacion": delegacion,
            "funcionario": funcionario,
        }

    # =====================================================
    # VALIDACIONES ADICIONALES
    # =====================================================

    def validate_nombre(self, value):
        nombre = value.strip()

        if not nombre:
            raise serializers.ValidationError(
                "Debe ingresar el nombre de la delegación."
            )

        return nombre

    def validate_sector(self, value):
        sector = value.strip()

        if not sector:
            raise serializers.ValidationError(
                "Debe ingresar el sector de la delegación."
            )

        return sector

    def validate_descripcion(self, value):
        descripcion = value.strip()

        if not descripcion:
            raise serializers.ValidationError(
                "Debe ingresar una descripción."
            )

        return descripcion
