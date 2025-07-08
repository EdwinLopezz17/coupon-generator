import streamlit as st
import pandas as pd
from services import data_validation
from io import BytesIO
from datetime import datetime

def show():
    st.title("📝 Generar Archivo ERP")

    if ("cupones_sku_validos" in st.session_state or
        "cupones_cat_validos" in st.session_state):

        productos_df = st.session_state.get("productos_df", pd.DataFrame())
        final_sku_df = st.session_state.get("cupones_sku_validos", pd.DataFrame())
        final_cat_df = st.session_state.get("cupones_cat_validos", pd.DataFrame())

        final_cat_df = data_validation.expand_category_coupons(final_cat_df, productos_df)
        final_sku_df = data_validation.merge_sku_with_products(final_sku_df, productos_df)

        final_erp_df = pd.concat([final_sku_df, final_cat_df], ignore_index=True)

        st.success(f"Archivo ERP generado con {len(final_erp_df)} registros.")
        with st.expander("Vista previa ERP"):
            st.dataframe(final_erp_df.head(20))

        output = BytesIO()
        final_erp_df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        st.download_button(
            label="⬇️ Descargar archivo ERP (.xlsx)",
            data=output,
            file_name=f"cupones_validados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No hay datos cargados para generar ERP.")
