import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils.timezone import make_aware

# 🔹 Configurar Django antes de acceder a la BD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto_webscraping.settings')  
django.setup()

from scraper.models import OposicionBOE  # Ahora Django reconocerá los modelos



# 📅 Generar la URL del BOE del día actual
# hoy = datetime.today().strftime("%Y/%m/%d")
# url = f"https://www.boe.es/boe/dias/{hoy}/"

url = "https://www.boe.es/boe/dias/2025/03/10/"  # Actualiza la fecha al día de la prueba

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 📌 Buscar la sección de Administración Local
sumario = soup.find("div", class_="sumario")
oposiciones_relevantes = []
nuevas_oposiciones = 0  # Contador de oposiciones guardadas

# 🔍 Lista de palabras clave para detectar oposiciones locales
palabras_clave = [
    "Administración Local", "Ayuntamiento", "Diputación", "Mancomunidad",
    "Ofertas de empleo", "Oposición", "Convocatoria",
    "Funcionario", "Personal funcionario", "Personal laboral", "Proceso selectivo"
]

if sumario:
    # 🔍 Filtrar secciones que contienen palabras clave
    for bloque in sumario.find_all(["h4", "h5"]):
        if any(palabra in bloque.text for palabra in palabras_clave):  # Verifica si alguna palabra clave está en el texto
            enlace_tag = bloque.find_next("a")  # Busca el enlace al PDF de la convocatoria
            enlace = "https://www.boe.es" + enlace_tag["href"] if enlace_tag else "Sin enlace"
            titulo = bloque.text.strip()

            # Guardar en la base de datos si no existe
            if not OposicionBOE.objects.filter(enlace=enlace).exists():
                nueva_oposicion = OposicionBOE(
                    titulo=titulo,
                    enlace=enlace,
                    fecha_publicacion=make_aware(datetime.today())
                )
                nueva_oposicion.save()
                nuevas_oposiciones += 1
                print(f"✅ Guardada en la BD: {titulo} -> {enlace}")

            oposiciones_relevantes.append((titulo, enlace))

    # 📢 Mostrar los resultados
    print(f"📌 Se encontraron {len(oposiciones_relevantes)} oposiciones en Administración Local.")
    print(f"📥 {nuevas_oposiciones} nuevas oposiciones guardadas en la BD.")

else:
    print("⚠️ No se encontró la sección de oposiciones en Administración Local.")