
from django import forms

from delegacionesApp.models import Delegacion
from .models import Funcionario


# =========================================================
# SIGED EVA 3 - FORMULARIO DE FUNCIONARIOS
# =========================================================

class FuncionarioForm(forms.ModelForm):

    class Meta:

        model = Funcionario

        fields = [
            "nombre",
            "cargo",
            "delegacion",
            "meta",
            "avance",
        ]

        labels = {
            "nombre": "Nombre del funcionario",
            "cargo": "Cargo del funcionario",
            "delegacion": "Delegación asignada",
            "meta": "Meta asignada",
            "avance": "Avance actual",
        }

        widgets = {

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre completo del funcionario",
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

            "delegacion": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "meta": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese la meta",
                    "min": 0,
                    "step": 1,
                }
            ),

            "avance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese el avance",
                    "min": 0,
                    "step": 1,
                }
            ),

        }

        help_texts = {
            "meta": "Cantidad total que debe cumplir el funcionario.",
            "avance": "Cantidad alcanzada hasta el momento.",
        }

    # =====================================================
    # CONFIGURACION INICIAL DEL FORMULARIO
    # =====================================================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Cargar las delegaciones disponibles desde MySQL.

        self.fields["delegacion"].queryset = (
            Delegacion.objects.all().order_by("nombre")
        )

        self.fields["delegacion"].empty_label = (
            "Seleccione una delegación"
        )

        # Valores por defecto para funcionarios nuevos.

        if not self.instance.pk:
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

        # Los valores no pueden ser negativos.

        if meta < 0:
            self.add_error(
                "meta",
                "La meta no puede ser negativa."
            )

        if avance < 0:
            self.add_error(
                "avance",
                "El avance no puede ser negativo."
            )

        # El avance no puede superar la meta.

        if meta >= 0 and avance >= 0 and avance > meta:
            self.add_error(
                "avance",
                "El avance no puede superar la meta asignada."
            )

        return datos
