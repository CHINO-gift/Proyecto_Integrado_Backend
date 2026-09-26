from django.db import models
from delegacionesApp.models import Delegacion


class Funcionario(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)

    delegacion = models.ForeignKey(
        Delegacion,
        on_delete=models.PROTECT,
        related_name='funcionarios'
    )

    meta = models.PositiveIntegerField(default=0)
    avance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

    @property
    def porcentaje(self):
        if self.meta > 0:
            return round((self.avance / self.meta) * 100)
        return 0

    class Meta:
        db_table = 'funcionarios'
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        ordering = ['nombre']