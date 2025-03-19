import os
import json
from django.shortcuts import render

# 📂 Ruta del archivo JSON con las oposiciones extraídas
json_file_path = os.path.join(os.path.dirname(__file__), "oposiciones.json")

def oposiciones_boe(request):
    """ Vista para mostrar las oposiciones extraídas del BOE desde JSON """

    oposiciones = []
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as file:
            try:
                oposiciones = json.load(file)  # Cargar los datos desde JSON
            except json.JSONDecodeError:
                pass  # Si el archivo está vacío o tiene un error, no cargar nada

    return render(request, "oposiciones_boe.html", {"oposiciones": oposiciones})

