import streamlit as st

# Set page config (must be the first Streamlit command)
st.set_page_config(page_title="🏠 Dashboard Inicio", layout="wide")

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
            st.info("Esta sección permite importar los datos CSV a la base de datos SQLite.")
            st.warning("Nota: Este proceso puede tardar unos segundos y sobrescribirá los datos existentes.")

            if st.button("Importar datos CSV a SQLite"):
                with st.spinner("Importando datos..."):
                    try:
                        # Show more detailed progress
                        progress_text = st.empty()
                        progress_text.text("Creando tablas en la base de datos...")

                        # Import data
                        progress_text.text("Importando datos desde archivos CSV...")
                        import_csv_data()

                        # Success message
                        progress_text.empty()
                        st.success("Datos importados correctamente a la base de datos SQLite.")
                        st.info("Ahora puedes navegar a las otras páginas para ver los datos.")
                    except Exception as e:
                        st.error(f"Error importando datos: {e}")
                        st.info("Asegúrate de que los archivos CSV estén en la carpeta 'data' y tengan el formato correcto.")
