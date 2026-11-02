
from django import forms

from funcionariosApp.models import Funcionario


# =========================================================
# SIGED EVA 3 - REGISTRO CONJUNTO
# DELEGACION + FUNCIONARIO INICIAL
# =========================================================


class FuncionarioInicialForm(forms.ModelForm):

    """
    Formulario para registrar un funcionario
    junto con una nueva delegacion.

    No solicita la delegacion porque esta
    sera creada durante la misma operacion.
    """

    class Meta:

        model = Funcionario

        fields = [
            "nombre",
            "cargo",
            "meta",
            "avance",
        ]

        labels = {
            "nombre": "Nombre del funcionario",
            "cargo": "Cargo del funcionario",
            "meta": "Meta asignada",
            "avance": "Avance actual",
        }

        widgets = {

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre completo",
                    "maxlength": 100,
                }
            ),

            "cargo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cargo que desempeña",
                    "maxlength": 100,
                }
            ),

            "meta": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": 1,
                }
            ),

            "avance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": 1,
                }
            ),
        }

        help_texts = {
            "meta": "Cantidad total que debe cumplir.",
            "avance": "Cantidad alcanzada hasta el momento.",
        }

    # =====================================================
    # VALORES INICIALES
    # =====================================================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if not self.is_bound and not self.instance.pk:

            self.fields["meta"].initial = 0
            self.fields["avance"].initial = 0

    # =====================================================
    # VALIDAR NOMBRE
    # =====================================================

    def clean_nombre(self):

        nombre = self.cleaned_data["nombre"].strip()

        if not nombre:

            raise forms.ValidationError(
                "Debe ingresar el nombre del funcionario."
            )

        return nombre

    # =====================================================
    # VALIDAR CARGO
    # =====================================================

    def clean_cargo(self):

        cargo = self.cleaned_data["cargo"].strip()

        if not cargo:

            raise forms.ValidationError(
                "Debe ingresar el cargo del funcionario."
            )

        return cargo

    # =====================================================
    # VALIDAR META Y AVANCE
    # =====================================================

    def clean(self):

        datos = super().clean()

        meta = datos.get("meta")
        avance = datos.get("avance")

        if meta is None or avance is None:
            return datos

        if avance > meta:

            self.add_error(
                "avance",
                "El avance no puede superar la meta asignada."
            )

        return datos
