from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from scraper.models import Oposicion, Ayuntamiento

def extraer_oposiciones(url=None):
    options = Options()
    options.add_argument("--headless")  # Para que no abra el navegador
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    if url:
        ayuntamientos = Ayuntamiento.objects.filter(url=url, activo=True)
    else:
        ayuntamientos = Ayuntamiento.objects.filter(activo=True)

    for ayuntamiento in ayuntamientos:
        print(f"🔍 Buscando oposiciones en: {ayuntamiento.nombre}")

        try:
            driver.get(ayuntamiento.url)
            time.sleep(5)  # Esperamos a que cargue el JS

            oposiciones = driver.find_elements(By.CSS_SELECTOR, "div.content h3 a")

            if not oposiciones:
                print(f"⚠️ No se encontraron oposiciones en {ayuntamiento.url}")
                continue

            for oposicion in oposiciones:
                titulo = oposicion.text.strip()
                enlace = oposicion.get_attribute("href")

                if not Oposicion.objects.filter(enlace=enlace).exists():
                    nueva_oposicion = Oposicion(
                        titulo=titulo,
                        entidad=ayuntamiento.nombre,
                        enlace=enlace
                    )
                    nueva_oposicion.save()
                    print(f"✅ Guardada: {titulo}")
                else:
                    print(f"⚠️ Ya existe: {titulo}")

        except Exception as e:
            print(f"❌ Error en {ayuntamiento.nombre}: {e}")

    driver.quit()

