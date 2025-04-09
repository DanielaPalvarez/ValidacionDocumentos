
# 🧾 Validación de Documentos con OCR

Este proyecto utiliza **Python + OCR (Tesseract)** para extraer y validar datos clave de documentos oficiales escaneados, como:

- Credencial del INE
- Factura de vehículo
- Tarjeta de circulación

Es útil para procesos de **automatización, verificación de identidad o registros vehiculares**, permitiendo comparar que los datos coincidan entre los documentos cargados.

---

## 🧠 Estructura del Proyecto

```
📁 ValidacionDocumentos
├── orc_ine.py               # OCR y extracción para INE (PDF escaneado)
├── factura.py               # OCR y extracción para factura de vehículo
├── tarjeta_circulacion.py   # OCR y extracción para tarjeta de circulación
├── comparador.py            # Compara los datos entre los documentos
├── Entregables/             # Carpeta donde colocar los PDFs reales
└── README.md                # Este archivo
```

---

## ⚙️ Requisitos

- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (instalado y en el PATH)
- [Poppler](https://blog.alivate.com.au/poppler-windows/) (para convertir PDFs a imágenes)

Instala las dependencias de Python:

```bash
pip install pytesseract pdf2image Pillow
```

---

## 🚀 ¿Cómo se usa?

1. Coloca tus archivos PDF escaneados dentro de la carpeta `Entregables/`
2. Ejecuta el script correspondiente:

### INE

```bash
python ine.py
```

### Factura

```bash
python factura.py
```

### Tarjeta de circulación

```bash
python tarjeta_circulacion.py
```

Cada script imprimirá el texto detectado por OCR y los campos extraídos.

---

## 📌 Datos extraídos por documento

### INE
- Nombre completo
- CURP
- Clave de elector
- Vigencia

### Factura
- Nombre del solicitante
- RFC emisor y receptor
- VIN (NIV)
- Marca, modelo, año
- Valor total de factura

### Tarjeta de circulación
- Nombre del titular
- Placas
- Uso (particular/público)
- Marca, modelo, año
- Vigencia


## 👩‍💻 Autores

Proyecto desarrollado por **Andrea Quiroz**, **Alan Mota**, **Daniela Pamelin**, **Diego Soria**, **Rubi Royval** 