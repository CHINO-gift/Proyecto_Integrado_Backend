from django.db import models


class Delegacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    sector = models.CharField(max_length=150)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'delegaciones'
        verbose_name = 'Delegación'
        verbose_name_plural = 'Delegaciones'
        ordering = ['nombre']