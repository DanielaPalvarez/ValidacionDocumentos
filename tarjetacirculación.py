from pdf2image import convert_from_path
from PIL import Image, ImageOps
import pytesseract
import re

def convertir_pdf_a_imagenes(ruta_pdf):
    return convert_from_path(ruta_pdf)

def preprocesar_imagen(imagen):
    imagen = imagen.convert('L')
    imagen = ImageOps.autocontrast(imagen)
    imagen = imagen.point(lambda x: 0 if x < 140 else 255, '1')
    return imagen

def extraer_texto_tarjeta(imagenes):
    textos = []
    for imagen in imagenes:
        imagen = preprocesar_imagen(imagen)
        texto = pytesseract.image_to_string(imagen, lang='spa')
        textos.append(texto)
    return textos

def parsear_datos_tarjeta(textos):
    datos = {
        "nombre": None,
        "placas": None,
        "vin": None,
        "marca": None,
        "modelo": None,
        "anio": None,
        "vigencia": None,
        "uso": None
    }

    texto = "\n".join(textos).upper()

    # Placas
    match_placas = re.search(r"PLACAS?:?\s*([A-Z0-9\-]{6,10})", texto)
    if match_placas:
        datos["placas"] = match_placas.group(1)

    # VIN
    match_vin = re.search(r"\b([A-HJ-NPR-Z0-9]{17})\b", texto)
    if match_vin:
        datos["vin"] = match_vin.group(1)

    # Marca y modelo
    match_auto = re.search(r"MARCA[\s:]*([A-Z]+).*?MODELO[\s:]*([A-Z0-9]+).*?AÑO[\s:]*([0-9]{4})", texto)
    if match_auto:
        datos["marca"] = match_auto.group(1)
        datos["modelo"] = match_auto.group(2)
        datos["anio"] = match_auto.group(3)

    # Vigencia
    match_vigencia = re.search(r"VIGENCIA[\s:]*([0-9]{4})", texto)
    if match_vigencia:
        datos["vigencia"] = match_vigencia.group(1)

    # Nombre
    match_nombre = re.search(r"NOMBRE[\s:]*([A-ZÁÉÍÓÚÑ\s]+)", texto)
    if match_nombre:
        datos["nombre"] = match_nombre.group(1).strip()

    # Uso
    match_uso = re.search(r"USO[\s:]*([A-Z]+)", texto)
    if match_uso:
        datos["uso"] = match_uso.group(1)

    return datos

def procesar_tarjeta(ruta_pdf):
    imagenes = convertir_pdf_a_imagenes(ruta_pdf)
    textos = extraer_texto_tarjeta(imagenes)

    print("\n--- TEXTO OCR DETECTADO ---")
    for i, t in enumerate(textos):
        print(f"\nPágina {i+1}:\n{t}\n")

    datos = parsear_datos_tarjeta(textos)
    return datos


if __name__ == "__main__":
    ruta = "tarjeta.pdf"
    resultado = procesar_tarjeta(ruta)
    print("Datos extraídos de la TARJETA DE CIRCULACIÓN:")
    for k, v in resultado.items():
        print(f"{k}: {v}")
