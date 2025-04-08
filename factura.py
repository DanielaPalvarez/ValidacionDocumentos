from pdf2image import convert_from_path
from PIL import Image, ImageOps
import pytesseract
import re
import os

def convertir_pdf_a_imagenes(ruta_pdf):
    return convert_from_path(ruta_pdf)

def preprocesar_imagen(imagen):
    imagen = imagen.convert('L')
    imagen = ImageOps.autocontrast(imagen)
    imagen = imagen.point(lambda x: 0 if x < 140 else 255, '1')
    return imagen

def extraer_texto_factura(imagenes):
    textos = []
    for imagen in imagenes:
        imagen = preprocesar_imagen(imagen)
        texto = pytesseract.image_to_string(imagen, lang='spa')
        textos.append(texto)
    return textos

def parsear_datos_factura(textos):
    datos = {
        "nombre_solicitante": None,
        "rfc_emisor": None,
        "rfc_receptor": None,
        "vin": None,
        "marca": None,
        "modelo": None,
        "anio": None,
        "total_factura": None
    }

    texto = "\n".join(textos).upper()

   
    rfc_pattern = r"\b([A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3})\b"
    rfc_matches = re.findall(rfc_pattern, texto)
    if len(rfc_matches) >= 2:
        datos["rfc_emisor"] = rfc_matches[0]
        datos["rfc_receptor"] = rfc_matches[1]

   
    match_total = re.search(r"TOTAL.*?\$?\s*([\d,]+\.\d{2})", texto)
    if match_total:
        datos["total_factura"] = match_total.group(1)

    
    match_vin = re.search(r"\b([A-HJ-NPR-Z0-9]{17})\b", texto)
    if match_vin:
        datos["vin"] = match_vin.group(1)

    
    match_auto = re.search(r"(MARCA|VEHÍCULO)[\s:]*([A-Z]+)\s+MODELO\s+(\d{4})", texto)
    if match_auto:
        datos["marca"] = match_auto.group(2)
        datos["anio"] = match_auto.group(3)

   
    match_nombre = re.search(r"NOMBRE[\s:]*([A-ZÁÉÍÓÚÑ\s]+)", texto)
    if match_nombre:
        datos["nombre_solicitante"] = match_nombre.group(1).strip()

    return datos

def procesar_factura(ruta_pdf):
    imagenes = convertir_pdf_a_imagenes(ruta_pdf)
    textos = extraer_texto_factura(imagenes)

    print("\n--- TEXTO OCR DETECTADO ---")
    for i, t in enumerate(textos):
        print(f"\nPágina {i+1}:\n{t}\n")

    datos = parsear_datos_factura(textos)
    return datos


if __name__ == "__main__":
    ruta = "Factura.pdf"  
    resultado = procesar_factura(ruta)
    print("Datos extraídos de la FACTURA:")
    for k, v in resultado.items():
        print(f"{k}: {v}")
