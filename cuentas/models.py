from django.contrib.auth.models import AbstractUser
from django.db import models


class Herramienta(models.Model):
    """Una actividad del front. El slug debe coincidir con el `id` de TOOLS en src/App.vue."""

    slug = models.SlugField(unique=True)
    nombre = models.CharField(max_length=80)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    """Agrupa usuarios y define a qué herramientas tienen acceso."""

    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)
    herramientas = models.ManyToManyField(Herramienta, blank=True, related_name='perfiles')

    class Meta:
        verbose_name_plural = 'perfiles'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    perfil = models.ForeignKey(
        Perfil, null=True, blank=True, on_delete=models.SET_NULL, related_name='usuarios'
    )

    def herramientas_permitidas(self):
        # Los superusuarios ven todo aunque no tengan perfil asignado.
        if self.is_superuser:
            return Herramienta.objects.all()
        if self.perfil_id is None:
            return Herramienta.objects.none()
        return self.perfil.herramientas.all()
