from django.urls import path
from .views import oposiciones_boe # Importa la vista correctamente

urlpatterns = [
    path("boe/", oposiciones_boe, name="oposiciones_boe"),
]
