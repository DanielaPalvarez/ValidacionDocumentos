from pdf2image import convert_from_path
from PIL import Image, ImageOps
import pytesseract
import re

def convertir_pdf_a_imagenes(ruta_pdf):
    """
    Convierte todas las páginas del PDF a imágenes.
    """
    return convert_from_path(ruta_pdf)

def preprocesar_imagen(imagen):
    imagen = imagen.convert('L')
    imagen = imagen.resize((imagen.width * 2, imagen.height * 2))
    imagen = ImageOps.autocontrast(imagen)
    imagen = imagen.point(lambda x: 0 if x < 160 else 255, '1')
    return imagen

def extraer_texto_ine(imagenes):
    """
    Extrae texto OCR de cada imagen de INE.
    """
    textos = []
    for i, imagen in enumerate(imagenes):
        imagen = preprocesar_imagen(imagen)
        texto = pytesseract.image_to_string(imagen, lang='spa')
        print(f"\n--- TEXTO OCR - PÁGINA {i+1} ---\n{texto}")
        textos.append(texto.upper())
    return textos

def parsear_datos_ine(textos):
    datos = {
        "nombre": None,
        "clave_elector": None,
        "curp": None,
        "vigencia": None,
    }

    texto = "\n".join(textos)

    # 1. Nombre 
    match_nombre = re.search(r"NOMBRE\s+([A-ZÁÉÍÓÚÑ\s]+)\n([A-ZÁÉÍÓÚÑ\s]+)\n([A-ZÁÉÍÓÚÑ\s]+)", texto)
    if match_nombre:
        nombre_completo = f"{match_nombre.group(1)} {match_nombre.group(2)} {match_nombre.group(3)}"
        datos["nombre"] = nombre_completo.strip()

    # 2. Clave de elector
    match_clave = re.search(r"CLAVE DE ELECTOR\s*([A-Z0-9]{18})", texto)
    if match_clave:
        datos["clave_elector"] = match_clave.group(1)

    # 3. CURP
    match_curp = re.search(r"CURP\s*([A-Z0-9]{18})", texto)
    if match_curp:
        datos["curp"] = match_curp.group(1)

    # 5. Vigencia
    match_vigencia = re.search(r"VIGENCIA\s*(\d{4})", texto)
    if match_vigencia:
        datos["vigencia"] = match_vigencia.group(1)

    return datos


def procesar_ine(ruta_pdf):
    """
    Flujo completo: PDF → imágenes → texto → datos extraídos
    """
    imagenes = convertir_pdf_a_imagenes(ruta_pdf)
    textos = extraer_texto_ine(imagenes)
    datos = parsear_datos_ine(textos)
    return datos

# Ejecución directa
if __name__ == "__main__":
    ruta = "ine.pdf"  # Cambia esto al nombre real de tu PDF
    resultado = procesar_ine(ruta)

    print("\n--- DATOS EXTRAÍDOS DEL INE ---")
    for k, v in resultado.items():
        print(f"{k}: {v}")
