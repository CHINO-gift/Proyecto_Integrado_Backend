from django.contrib import admin
from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'cargo',
        'delegacion',
        'meta',
        'avance',
    )

    search_fields = (
        'nombre',
        'cargo',
        'delegacion__nombre',
    )

    list_filter = (
        'delegacion',
        'cargo',
    )

    ordering = ('nombre',)