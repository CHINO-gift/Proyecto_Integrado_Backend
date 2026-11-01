
from django import forms

from .models import Delegacion


# =========================================================
# SIGED EVA 3 - FORMULARIO DE DELEGACIONES
# =========================================================

class DelegacionForm(forms.ModelForm):

    class Meta:

        model = Delegacion

        fields = [
            "nombre",
            "sector",
            "descripcion",
        ]

        labels = {
            "nombre": "Nombre de la delegación",
            "sector": "Sector",
            "descripcion": "Descripción",
        }

        widgets = {

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de la delegación",
                    "maxlength": 100,
                }
            ),

            "sector": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Sector municipal",
                    "maxlength": 150,
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descripción de la delegación",
                    "rows": 4,
                }
            ),
        }

    # =====================================================
    # VALIDAR NOMBRE
    # =====================================================

    def clean_nombre(self):

        nombre = self.cleaned_data["nombre"].strip()

        if not nombre:
            raise forms.ValidationError(
                "Debe ingresar el nombre de la delegación."
            )

        return nombre

    # =====================================================
    # VALIDAR SECTOR
    # =====================================================

    def clean_sector(self):

        sector = self.cleaned_data["sector"].strip()

        if not sector:
            raise forms.ValidationError(
                "Debe ingresar el sector de la delegación."
            )

        return sector

    # =====================================================
    # VALIDAR DESCRIPCIÓN
    # =====================================================

    def clean_descripcion(self):

        descripcion = self.cleaned_data["descripcion"].strip()

        if not descripcion:
            raise forms.ValidationError(
                "Debe ingresar una descripción."
            )

        return descripcion
