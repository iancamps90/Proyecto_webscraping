import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils.timezone import make_aware
from scraper.models import Oposicion, Ayuntamiento

def extraer_oposiciones():
    ayuntamientos = Ayuntamiento.objects.filter(activo=True)  # Solo los activos

    for ayuntamiento in ayuntamientos:
        print(f"🔍 Buscando oposiciones en: {ayuntamiento.nombre}")

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(ayuntamiento.url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Error al acceder a {ayuntamiento.url}")
            continue

        soup = BeautifulSoup(response.text, "lxml")
        
        # Este código hay que adaptarlo a cada web de ayuntamiento
        oposiciones = soup.find_all("div", class_="oposicion")

        for oposicion in oposiciones:
            try:
                titulo = oposicion.find("h2").text.strip()
                entidad = ayuntamiento.nombre
                fecha_pub = datetime.strptime(oposicion.find("span", class_="fecha").text.strip(), "%d/%m/%Y")
                fecha_pub = make_aware(fecha_pub)  
                enlace = oposicion.find("a")["href"]

                if not Oposicion.objects.filter(enlace=enlace).exists():
                    nueva_oposicion = Oposicion(
                        titulo=titulo,
                        entidad=entidad,
                        fecha_publicacion=fecha_pub,
                        enlace=enlace
                    )
                    nueva_oposicion.save()
                    print(f"✅ Guardada: {titulo}")
                else:
                    print(f"⚠️ Ya existe: {titulo}")

            except Exception as e:
                print(f"⚠️ Error en {ayuntamiento.nombre}: {e}")
