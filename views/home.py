import streamlit as st

def show():
    st.title("🎫 Validador de Cupones ERP")
    st.markdown("""
    Bienvenido al **Validador de Cupones ERP**. Esta aplicación te permite:

    - **Cargar la base de productos**.
    - **Cargar cupones por producto (SKU)**.
    - **Cargar cupones por categoría**.
    - Validar datos automáticamente.
    - Generar archivo ERP.
    - Generar cupones PDF físicos o digitales.
    
    Usa el menú lateral para navegar.
    """)
