import streamlit as st

# Set page config (must be the first Streamlit command)
st.set_page_config(page_title="🏠 Dashboard Inicio", layout="wide")

import sys
import os
from pathlib import Path

# Add parent directory to path so we can import auth modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from auth.authenticator import check_authentication, logout_button

# ⚠️ Ya no se necesita crear la base de datos local ni importar CSVs

# Check authentication
is_authenticated, username, name, authenticator = check_authentication()

if is_authenticated:
    # Show logout button in sidebar
    with st.sidebar:
        st.write(f"👋 Hola, {name}")
        logout_button(authenticator)

    # Main content
    st.title("🏠 Bienvenido al Dashboard de Entrenamiento")

    st.markdown("Usa el menú lateral izquierdo para navegar entre las páginas 📊.")

    # Admin section
    if username == "admin":
        st.subheader("🔧 Administración")

        # Información administrativa (pero sin botón de carga de CSV)
        with st.expander("Información del Sistema"):
            st.info("La aplicación ahora está conectada a una base de datos MySQL.")
            st.write("📦 Los datos deben estar precargados en MySQL.")
            st.write("🔄 Puedes gestionar la carga de datos usando scripts externos de ETL.")
