import streamlit as st
import pandas as pd
from services import pdf_generator

def show():
    st.title("🎫 Generar Cupones PDF")

    erp_file = st.file_uploader(
        "Sube el archivo ERP (.xlsx) para generar cupones",
        type=["xlsx"]
    )

    if erp_file:
        erp_df = pd.read_excel(erp_file)
        erp_df.columns = erp_df.columns.str.strip()

        with st.expander("Vista previa ERP cargado"):
            st.dataframe(erp_df.head(10))

        opcion = st.radio(
            "¿Deseas generar cupones por categoría o por producto?",
            ["Por categoría", "Por producto (SKU)"]
        )

        if opcion == "Por categoría":
            categorias = erp_df['Categoría'].dropna().unique().tolist()
            categoria_sel = st.selectbox("Selecciona categoría:", categorias)
            num_cupones = st.number_input("¿Cuántos cupones deseas generar?", min_value=1, step=1, value=1)
            selection = categoria_sel
        else:
            productos = erp_df['Código Producto'].dropna().unique().tolist()
            producto_sel = st.selectbox("Selecciona el Código de Producto (SKU):", productos)
            num_cupones = st.number_input("¿Cuántos cupones deseas generar?", min_value=1, step=1, value=1)
            selection = producto_sel

        farmacia_nombre = st.text_input(
            "Nombre de la Farmacia que aparecerá en el cupón",
            value="Ahumada"
        )

        if st.button("Generar cupones PDF"):
            zip_file = pdf_generator.generate_coupons_pdf(
                erp_df,
                opcion,
                selection,
                num_cupones,
                farmacia_nombre
            )

            st.download_button(
                label="⬇️ Descargar Cupones en ZIP",
                data=zip_file,
                file_name=f"cupones_generados.zip",
                mime="application/zip"
            )
            st.success("✅ Cupones generados correctamente.")
