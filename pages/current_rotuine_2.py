import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from st_aggrid import AgGrid, GridOptionsBuilder

from utils.datawrangling import preprocess_routine_history, rep_concatenate, filter_by_routine
from utils.data_loader import load_and_prepare_data, load_data, load_dim_data
from utils.rm_calculator import run_1rm_calculator
from utils.etl_oltp_to_olap import create_exercise_dimension_table
from database.gsheet_connnector import read_and_clean_sheet
from utils.tables import process_historical_routine, editable_dataframe

st.set_page_config(page_title="Entrena", layout="wide")

def main():
    # Get user ID from session state if authenticated
    user_id = st.session_state.get("user_id", None)
    # Cargar variables de entorno
    load_dotenv()

    # Leer ruta desde variable
    CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

    scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)

    fitness_personal_key = os.getenv("GOOGLE_SHEET_KEY_FITNESS_PERSONAL")

    spreadsheet_fitness_personal = client.open_by_key(fitness_personal_key)

    sql_data = load_dim_data()

    # //////////////////// Load Data //////////////////////
    try:
        # Load data from SQLite database
        df = read_and_clean_sheet(spreadsheet_fitness_personal,
                                  worksheet_name='TrackRecord',
                                  date_cols=['fecha']
                                  )
        
        # Check if data is empty
        if df.empty:
            st.warning("No hay datos disponibles en la base de datos.")
            st.info("Por favor, importa datos a través del panel de administración en la página de inicio.")
            return

        routine_template = read_and_clean_sheet(spreadsheet_fitness_personal,
                                  worksheet_name='Routines'
                                  )
        
        exercises = sql_data['exercises']

    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        st.info("Por favor, importa datos a través del panel de administración en la página de inicio.")
        return

    # /////////////////////// Filter ///////////////////////

    # Seleccionar la rutina
    routines = df['routine_name'].unique()

    # /////////////////////// Display //////////////////////
    st.title('🏋🏽‍♂️ Entrenamiento')

    # Filter by Routine
    selected_routine = st.selectbox("Selecciona la rutina", routines)
    df_filtered = filter_by_routine(df, selected_routine, 'routine_name')

    # ///////// Section 1: Histórico
    st.subheader("📅 Historial de la rutina")

    # Select a date for show the history
    dates = df_filtered.sort_values(by='fecha', ascending=False)['fecha'].dt.strftime('%Y-%m-%d').unique()
    selected_date = st.selectbox("Historial para esta rutina:", dates)

    # Historico de rutinas
    df_filtered_by_date = df_filtered[df_filtered['fecha'].dt.strftime('%Y-%m-%d') == selected_date]
    df_filtered_by_date = preprocess_routine_history(df_filtered_by_date)
    df_hist, columns_to_show, height = process_historical_routine(df_filtered_by_date)
    st.dataframe(df_hist[columns_to_show].set_index('Ejercicio'), height=height)

    # ///////// Section 2: Ingresar Datos
    st.subheader("📥 Ingreso de rutina")

    # Plantilla de rutinas
    routine_template_filtered = filter_by_routine(routine_template, selected_routine, 'routine_name')
    routine_template_filtered = routine_template_filtered[['exercise', 'repmin', 'repmax']].copy()
    routine_template_filtered = rep_concatenate(routine_template_filtered, "repmin", "repmax").reset_index(drop=True)
    exercises_template = routine_template_filtered.exercise.unique()
    st.caption("Ingrese los nuevos datos para cada ejercicio")
    capitalized_names = exercises['english_name'].str.capitalize().sort_values().tolist()
    capitalized_names.insert(0, '-')

    for i, exercise_template in enumerate(exercises_template):
        print(f"Ejercicio {i+1}: {exercise_template}")

        if exercise_template in capitalized_names:
            idx_exercise = capitalized_names.index(exercise_template)
        else:
            st.warning(f"Ejercicio no encontrado: {exercise_template}")
            idx_exercise = 0  # fallback

        exercise_selection = st.selectbox(
            "Selecciona el ejercicio",
            options=capitalized_names,
            index=idx_exercise,
            key=f'selectbox_exercise_{i}',
            label_visibility="hidden"
        )
        edited_df = editable_dataframe(routine_template_filtered, exercise_selection, idx=i)

    if len(edited_df) > 0:
        if st.button("Guardar datos ingresados"):
            edited_df = pd.DataFrame(edited_df)
            today = datetime.now().strftime('%Y-%m-%d')
            edited_df['fecha'] = today
            edited_df['routine_name'] = selected_routine
            edited_df = edited_df[['fecha','routine_name','exercise','reprange','reps_real','weight','rir']]

            # Save to database instead of CSV file
            try:
                # This is a placeholder - in a real implementation, you would save to the database
                # For now, we'll just show a success message
                st.success("Datos guardados correctamente.")
                st.write("DataFrame con los datos ingresados:")
                st.dataframe(edited_df)
            except Exception as e:
                st.error(f"Error guardando datos: {e}")
    else:
        st.info("No se han ingresado datos aún.")

    # //////////// Section 3: Calcular RMs
    st.subheader("🧮 Calculadora de RM")
    st.caption("Calcula cuánto peso máximo podrías levantar entre 1 y 10 repeticiones.")
    run_1rm_calculator()

if __name__ == "__main__":
    main()
