import os
import sys
import json
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils.timezone import make_aware

# 🔹 Configurar Django antes de acceder a la BD
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Ir un nivel arriba
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from scraper.models import OposicionBOE  # Ahora Django reconocerá los modelos



# 📅 Generar la URL del BOE del día actual
hoy = datetime.today().strftime("%Y/%m/%d")
url = f"https://www.boe.es/boe/dias/{hoy}/"

#url = "https://www.boe.es/boe/dias/2025/03/19/"  # Actualiza la fecha al día de la prueba

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 📌 Buscar la sección de sumario
sumario = soup.find("div", class_="sumario")
oposiciones_relevantes = []

# 📌 Lista de palabras clave para detectar oposiciones
palabras_clave = [
    "Administración Local", "Ayuntamiento", "Diputación", "Concursos",
    "Ofertas de empleo", "Oposición", "Convocatoria",
    "Funcionario", "Personal funcionario", "Personal laboral", "Proceso selectivo"
]

# 📂 Archivo donde guardaremos los datos
json_file_path = os.path.join(os.path.dirname(__file__), "oposiciones.json")

# 🔍 Cargar datos previos si existen
if os.path.exists(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        try:
            oposiciones_relevantes = json.load(file)
        except json.JSONDecodeError:
            oposiciones_relevantes = []
else:
    oposiciones_relevantes = []

if sumario:
    ministerio_actual = None
    tipo_oferta_actual = None
    descripcion_actual = None
    enlace_actual = None

    for bloque in sumario.find_all(["h4", "h5", "ul", "div"]):
        # 📌 Extraer ministerio (h4)
        if bloque.name == "h4":
            ministerio_actual = bloque.text.strip()

        # 📌 Extraer tipo de oferta (h5)
        elif bloque.name == "h5":
            tipo_oferta_actual = bloque.text.strip()

        # 📌 Extraer la descripción dentro de `ul > li class="dispo" > p`
        elif bloque.name == "ul":
            dispo = bloque.find("li", class_="dispo")
            if dispo:
                descripcion_tag = dispo.find("p")
                descripcion_actual = descripcion_tag.text.strip() if descripcion_tag else "Sin descripción"

        # 📌 Extraer enlace al PDF dentro de `div class="enlacesDoc" > ul > li class="puntoPDF" > a`
        elif bloque.name == "div" and "enlacesDoc" in bloque.get("class", []):
            enlace_tag = bloque.find("a")
            enlace_actual = "https://www.boe.es" + enlace_tag["href"] if enlace_tag else "Sin enlace"

        # 📌 Guardar la información en JSON evitando duplicados
        if ministerio_actual and tipo_oferta_actual and descripcion_actual and enlace_actual:
            if any(palabra in tipo_oferta_actual for palabra in palabras_clave):
                nueva_oposicion = {
                    "titulo": tipo_oferta_actual,
                    "ministerio": ministerio_actual,
                    "descripcion": descripcion_actual,
                    "enlace": enlace_actual,
                    "fecha_publicacion": hoy,
                    "fuente": "BOE"
                }

                # Verificar que no exista ya el enlace en el JSON
                if not any(op["enlace"] == nueva_oposicion["enlace"] for op in oposiciones_relevantes):
                    oposiciones_relevantes.append(nueva_oposicion)
                    print(f"✅ Guardada en JSON: {tipo_oferta_actual} -> {enlace_actual}")

    # 📂 Guardar en el archivo JSON
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(oposiciones_relevantes, file, indent=4, ensure_ascii=False)

    # 📢 Mostrar los resultados
    print(f"📌 Se encontraron {len(oposiciones_relevantes)} oposiciones en el BOE.")

else:
    print("⚠️ No se encontró la sección de oposiciones en el BOE.")