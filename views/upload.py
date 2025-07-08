import streamlit as st
import pandas as pd
from services import data_validation

def show():
    st.title("📂 Cargar Archivos")

    productos_file = st.file_uploader(
        "Sube el archivo Excel con la base de productos",
        type=["xlsx"],
        key="prod_file"
    )

    cupones_sku_file = st.file_uploader(
        "Sube el archivo Excel con cupones por producto (SKU)",
        type=["xlsx"],
        key="sku_file"
    )

    cupones_categoria_file = st.file_uploader(
        "Sube el archivo Excel con cupones por categoría",
        type=["xlsx"],
        key="cat_file"
    )

    if productos_file:
        productos_df = pd.read_excel(productos_file)
        productos_df.columns = productos_df.columns.str.strip()
        st.session_state["productos_df"] = productos_df

        with st.expander("✅ Vista previa: Base de productos"):
            st.dataframe(productos_df.head(10))

    if cupones_sku_file and "productos_df" in st.session_state:
        productos_df = st.session_state["productos_df"]
        cupones_sku_df, errores_sku_df = data_validation.validate_sku_coupons(
            cupones_sku_file,
            productos_df
        )

        with st.expander("✅ Vista previa: Cupones por SKU"):
            st.dataframe(cupones_sku_df.head(10))

        if not errores_sku_df.empty:
            st.warning("⚠️ Hay errores en cupones por producto.")
            st.dataframe(errores_sku_df)
        else:
            st.success("✅ No se encontraron errores en cupones por producto.")

        cupones_sku_validos = cupones_sku_df[cupones_sku_df['Error'] == ""]
        st.session_state["cupones_sku_validos"] = cupones_sku_validos

    if cupones_categoria_file and "productos_df" in st.session_state:
        productos_df = st.session_state["productos_df"]
        cupones_cat_df, errores_cat_df = data_validation.validate_category_coupons(
            cupones_categoria_file,
            productos_df
        )

        with st.expander("✅ Vista previa: Cupones por Categoría"):
            st.dataframe(cupones_cat_df.head(10))

        if not errores_cat_df.empty:
            st.warning("⚠️ Hay errores en cupones por categoría.")
            st.dataframe(errores_cat_df)
        else:
            st.success("✅ No se encontraron errores en cupones por categoría.")

        cupones_cat_validos = cupones_cat_df[cupones_cat_df['Error'] == ""]
        st.session_state["cupones_cat_validos"] = cupones_cat_validos
