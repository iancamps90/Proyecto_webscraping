from django.db import models

#scraper boe
class OposicionBOE(models.Model):
    titulo = models.CharField(max_length=255)  # Título de la oposición
    enlace = models.URLField(unique=True)  # Enlace al PDF de la convocatoria
    fecha_publicacion = models.DateField()  # Fecha en la que se publicó en el BOE
    fuente = models.CharField(max_length=100, default="BOE")  # Fuente de la convocatoria

    def __str__(self):
        return f"{self.titulo} - {self.fecha_publicacion}"
    
    
#scraper opo 
class Oposicion(models.Model):
    CATEGORIAS = [
        ('Administrativo', 'Administrativo'),
        ('Policía Local', 'Policía Local'),
        ('Bomberos', 'Bomberos'),
        ('Sanidad', 'Sanidad'),
        ('Educación', 'Educación'),
        ('Ingeniería', 'Ingeniería'),
        ('Otros', 'Otros')
    ]
    
    titulo = models.CharField(max_length=255)
    entidad = models.CharField(max_length=255)
    comunidad = models.CharField(
        max_length=100,
        default="Valencia"  # 🔹 Agregamos un valor por defecto para evitar errores
    )
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIAS,
        default="Otros"  # 🔹 Valor por defecto para evitar errores en migración
    )
    fecha_publicacion = models.DateField()
    fecha_limite = models.DateField(null=True, blank=True)
    requisitos = models.TextField(blank=True)
    enlace = models.URLField(unique=True)

    def __str__(self):
        return f"{self.titulo} - {self.entidad} ({self.categoria})"


#scraper ayuntamientos
class Ayuntamiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)  # Nombre del ayuntamiento
    url = models.URLField(unique=True)  # Página donde publica oposiciones
    comunidad = models.CharField(
        max_length=100, 
        choices=[
        ('Andalucía', 'Andalucía'),
        ('Aragón', 'Aragón'),
        ('Asturias', 'Asturias'),
        ('Cantabria', 'Cantabria'),
        ('Castilla-La Mancha', 'Castilla-La Mancha'),
        ('Castilla y León', 'Castilla y León'),
        ('Cataluña', 'Cataluña'),
        ('Extremadura', 'Extremadura'),
        ('Galicia', 'Galicia'),
        ('Madrid', 'Madrid'),
        ('Murcia', 'Murcia'),
        ('Navarra', 'Navarra'),
        ('La Rioja', 'La Rioja'),
        ('País Vasco', 'País Vasco'),
        ('Valencia', 'Valencia'),
        ('Ceuta', 'Ceuta'),
        ('Melilla', 'Melilla')
    ],
        default='Valencia'  # Establecemos un valor por defecto para evitar el error
    )
    activo = models.BooleanField(default=True)  # Para desactivar ayuntamientos si fallan

    def __str__(self):
        return f"{self.nombre} ({self.comunidad})"