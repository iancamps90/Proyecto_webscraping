from django.contrib import admin
from .models import OposicionBOE, Oposicion, Ayuntamiento

# 🔹 Registrar modelos en el panel de administración
admin.site.register(OposicionBOE)
admin.site.register(Oposicion)
admin.site.register(Ayuntamiento)

