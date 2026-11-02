
from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


# =========================================================
# SIGED EVA 3 - GESTION DE USUARIOS
# =========================================================

User = get_user_model()

PERFILES_SIGED = [
    "Administrador",
    "Supervisor",
    "Administrativo",
]


# =========================================================
# VALIDAR CORREO ELECTRONICO
# =========================================================

def validar_correo_unico(correo, usuario_id=None):

    correo = correo.strip().lower()

    usuarios = User.objects.filter(
        email__iexact=correo
    )

    if usuario_id is not None:
        usuarios = usuarios.exclude(
            pk=usuario_id
        )

    if usuarios.exists():
        raise forms.ValidationError(
            "Este correo electrónico ya está "
            "registrado en SIGED."
        )

    return correo


# =========================================================
# FORMULARIO - CREAR USUARIO
# =========================================================

class UsuarioCreacionForm(UserCreationForm):

    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        max_length=254
    )

    perfil = forms.ModelChoiceField(
        queryset=Group.objects.filter(
            name__in=PERFILES_SIGED
        ).order_by("name"),
        label="Perfil del usuario",
        empty_label="Seleccione un perfil",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    class Meta(UserCreationForm.Meta):

        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Correo electrónico",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for nombre in [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]:

            self.fields[nombre].widget.attrs.update({
                "class": "form-control"
            })

        self.fields["username"].widget.attrs.update({
            "placeholder": "Nombre de usuario"
        })

        self.fields["first_name"].widget.attrs.update({
            "placeholder": "Nombres"
        })

        self.fields["last_name"].widget.attrs.update({
            "placeholder": "Apellidos"
        })

        self.fields["email"].widget.attrs.update({
            "placeholder": "correo@ejemplo.com"
        })

        self.fields["password1"].widget.attrs.update({
            "placeholder": "Contraseña inicial",
            "autocomplete": "new-password",
        })

        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirmar contraseña",
            "autocomplete": "new-password",
        })

    def clean_email(self):

        return validar_correo_unico(
            self.cleaned_data["email"]
        )


# =========================================================
# FORMULARIO - MODIFICAR USUARIO
# =========================================================

class UsuarioEdicionForm(forms.ModelForm):

    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        max_length=254
    )

    perfil = forms.ModelChoiceField(
        queryset=Group.objects.filter(
            name__in=PERFILES_SIGED
        ).order_by("name"),
        label="Perfil del usuario",
        empty_label="Seleccione un perfil",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
        ]

        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Correo electrónico",
            "is_active": "Cuenta activa",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for nombre in [
            "username",
            "first_name",
            "last_name",
            "email",
        ]:

            self.fields[nombre].widget.attrs.update({
                "class": "form-control"
            })

        self.fields["is_active"].widget.attrs.update({
            "class": "form-check-input"
        })

        if self.instance.pk:

            perfil_actual = self.instance.groups.filter(
                name__in=PERFILES_SIGED
            ).first()

            if perfil_actual:
                self.fields["perfil"].initial = (
                    perfil_actual
                )

    def clean_email(self):

        return validar_correo_unico(
            self.cleaned_data["email"],
            usuario_id=self.instance.pk
        )
