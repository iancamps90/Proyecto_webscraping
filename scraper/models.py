from django.db import models

class Oposicion(models.Model):
    titulo = models.CharField(max_length=255)  # Título de la oposición
    entidad = models.CharField(max_length=255)  # Ayuntamiento o institución convocante
    fecha_publicacion = models.DateField()  # Fecha en que se publicó
    fecha_limite = models.DateField(null=True, blank=True)  # Último día de inscripción
    requisitos = models.TextField(blank=True)  # Descripción de requisitos
    enlace = models.URLField(unique=True)  # URL a la convocatoria oficial

    def __str__(self):
        return f"{self.titulo} - {self.entidad}"


class Ayuntamiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)  # Nombre del ayuntamiento
    url = models.URLField(unique=True)  # Página donde publica oposiciones
    activo = models.BooleanField(default=True)  # Para desactivar ayuntamientos si fallan

    def __str__(self):
        return self.nombre