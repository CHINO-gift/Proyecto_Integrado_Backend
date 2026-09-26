from django.contrib import admin
from .models import Delegacion


@admin.register(Delegacion)
class DelegacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'sector')
    search_fields = ('nombre', 'sector', 'descripcion')
    ordering = ('nombre',)