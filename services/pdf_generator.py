import tempfile
import os
from zipfile import ZipFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
import barcode
from barcode.writer import ImageWriter
from datetime import datetime
from PIL import Image
from io import BytesIO

def generate_coupons_pdf(erp_df, opcion, selection, num_cupones, farmacia_nombre):
    with tempfile.TemporaryDirectory() as tempdir:
        pdf_files = []

        for i in range(num_cupones):
            numero_base = "271505"
            numero_cupon = f"{i+1:06d}"
            ean_number = numero_base + numero_cupon[-6:]

            ean = barcode.get('ean13', ean_number, writer=ImageWriter())
            barcode_filename_base = os.path.join(tempdir, f"barcode_{i}")
            barcode_filename = ean.save(barcode_filename_base)

            pdf_filename = os.path.join(tempdir, f"cupon_{i+1}.pdf")
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            width, height = letter

            magenta_color = colors.HexColor("#c71585")
            black_color = colors.black

            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(magenta_color)
            c.drawCentredString(width/2, height - 60, "Cupón de descuento")

            c.setLineWidth(2)
            c.setStrokeColor(magenta_color)
            c.line(50, height - 70, width - 50, height - 70)

            c.setFillColor(black_color)
            c.setFont("Helvetica", 12)

            if opcion == "Por categoría":
                producto_texto = selection
                descuento_info = erp_df[erp_df['Categoría'] == selection].iloc[0]
            else:
                row_info = erp_df[erp_df['Código Producto'] == selection].iloc[0]
                producto_texto = row_info['Productos']
                descuento_info = row_info

            fecha_actual = datetime.today().strftime("%d-%m-%Y")

            c.drawString(70, height - 110, f"Medicamento(s) : {producto_texto}")
            c.drawString(70, height - 130, f"Farmacia      : {farmacia_nombre}")
            c.drawString(70, height - 150, f"Fecha emisión : {fecha_actual}")

            descuento_tipo = descuento_info['Tipo Descuento']
            descuento_valor = descuento_info['Valor']

            if descuento_tipo.lower() == "porcentaje":
                texto_descuento = f"{int(descuento_valor)}% Dcto."
            else:
                texto_descuento = f"S/. {descuento_valor:.2f} Dcto."

            c.setFont("Helvetica-Bold", 26)
            c.setFillColor(magenta_color)
            c.drawCentredString(width/2, height - 220, texto_descuento)

            with Image.open(barcode_filename) as img:
                img_width, img_height = img.size
                img_ratio = img_height / img_width
                desired_width = 80 * mm
                desired_height = desired_width * img_ratio

                c.drawImage(
                    barcode_filename,
                    (width - desired_width)/2,
                    height - 350,
                    width=desired_width,
                    height=desired_height
                )

            aviso = "El uso de este cupón está sujeto a términos y condiciones. No acumulable con otras promociones."
            c.setFont("Helvetica-Oblique", 8)
            c.setFillColor(black_color)
            c.drawString(50, height - 380, aviso)

            c.showPage()
            c.save()

            pdf_files.append(pdf_filename)

        zip_path = os.path.join(tempdir, "cupones_generados.zip")

        with ZipFile(zip_path, "w") as zipf:
            for pdf in pdf_files:
                zipf.write(pdf, os.path.basename(pdf))

        with open(zip_path, "rb") as f:
            zip_bytes = f.read()

        return BytesIO(zip_bytes)
