import streamlit as st
from views import home, upload, erp, generate_coupons

st.set_page_config(
    page_title="Validador de Cupones ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
menu = st.sidebar.radio(
    "Menú de navegación",
    [
        "🏠 Inicio",
        "📂 Cargar Archivos",
        "📝 Generar Archivo ERP",
        "🎫 Generar Cupones PDF"
    ]
)

# Routing
if menu == "🏠 Inicio":
    home.show()
elif menu == "📂 Cargar Archivos":
    upload.show()
elif menu == "📝 Generar Archivo ERP":
    erp.show()
elif menu == "🎫 Generar Cupones PDF":
    generate_coupons.show()
