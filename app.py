import streamlit as st
from views import home, upload, erp, generate_coupons

st.set_page_config(
    page_title="Validador de Cupones ERP",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## Menú de navegación")

menu_items = {
    "Inicio": home.show,
    "Cargar Archivos": upload.show,
    "Generar Archivo ERP": erp.show,
    "Generar Cupones PDF": generate_coupons.show,
}

selection = st.sidebar.radio("", list(menu_items.keys()))

# Routing
menu_items[selection]()
