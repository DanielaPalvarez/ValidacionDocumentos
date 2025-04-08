import cv2
import pytesseract
import re


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\'

def preprocesar_imagen(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, binarizada = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    procesada = cv2.medianBlur(binarizada, 3)

    return procesada

def extraer_texto(imagen_procesada):
    texto = pytesseract.image_to_string(imagen_procesada, lang='spa')
    return texto

def extraer_campos_ine(texto):
    resultados = {}

    # CURP 
    patron_curp = r'\b[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d\b'
    curp = re.search(patron_curp, texto)
    resultados['CURP'] = curp.group() if curp else 'No encontrado'

    # Clave de Elector 
    patron_clave_elector = r'\b[A-Z]{6}\d{8}[HM]\d{3}\b'
    clave_elector = re.search(patron_clave_elector, texto)
    resultados['Clave Elector'] = clave_elector.group() if clave_elector else 'No encontrado'

    # Año de registro 
    patron_registro = r'Registro[:\s]+(\d{4})'
    registro = re.search(patron_registro, texto, re.IGNORECASE)
    resultados['Año Registro'] = registro.group(1) if registro else 'No encontrado'

    # Nombre del Titular 
    patron_nombre = r'Nombre[:\s]+([A-Z\s]+)\n'
    nombre = re.search(patron_nombre, texto, re.IGNORECASE)
    resultados['Nombre'] = nombre.group(1).strip() if nombre else 'No encontrado'

    return resultados

def main(ruta_imagen):
    imagen_procesada = preprocesar_imagen(ruta_imagen)
    texto_extraido = extraer_texto(imagen_procesada)
    
    print("\nTexto extraído del INE:\n")
    print(texto_extraido)

    campos = extraer_campos_ine(texto_extraido)

    print("\nInformación estructurada extraída:\n")
    for campo, valor in campos.items():
        print(f"{campo}: {valor}")

if __name__ == "__main__":
    ruta_imagen = 'C:\Users\Daniela Pamelin\Downloads\ValidacionDocumentos\Entregables\Caso 1\TK 62853-2.pdf'
    main(ruta_imagen)
