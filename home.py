import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import auth modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from auth.authenticator import check_authentication, logout_button, init_auth_tables
from database.db_setup import create_database, import_csv_data

# Initialize database and auth tables if they don't exist
try:
    create_database()
    init_auth_tables()
except Exception as e:
    st.error(f"Error initializing database: {e}")

# Set page config
st.set_page_config(page_title="🏠 Dashboard Inicio", layout="wide")

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

        # Database management
        with st.expander("Gestión de Base de Datos"):
            if st.button("Importar datos CSV a SQLite"):
                with st.spinner("Importando datos..."):
                    try:
                        import_csv_data()
                        st.success("Datos importados correctamente")
                    except Exception as e:
                        st.error(f"Error importando datos: {e}")
