import streamlit as st
import pandas as pd
from datetime import timedelta, datetime
from utils.data_loader import load_data, filter_by_date, get_date_filters
from utils.kpis import compute_kpis, display_kpis
from utils.tables import reorder_columns, calculate_summary_table, display_summary_table, compute_difference_between_kpis
from utils.charts import plot_line_vs_bar, display_exercise_tags, labels, plot_muscle_analysis
from utils.dashboard_utils import load_common_resources

st.set_page_config(page_title="Análisis Muscular", layout="wide")

st.title("Análisis Muscular")

def main():
    df, df_muscles = load_data("data/20250405_track_record_aggregated.csv", "data/20250405_track_record_breakdown_muscles.csv")

    # ////////////////// Filtros ////////////////////////
    min_date, max_date = get_date_filters(df)
    # Default range: last 6 weeks
    today = datetime.today().date()
    default_start = today - timedelta(weeks=6)
    default_end = today

    # Convert Timestamp to .date()
    min_date = min_date.date()
    max_date = max_date.date()

    # Bound defaults to data limits
    default_start = max(default_start, min_date)
    default_end = min(default_end, max_date)

    try:
        start_date, end_date = st.sidebar.date_input(
            "Rango de fechas", 
            value=[default_start, default_end],
            min_value=min_date, max_value=max_date
        )

        period_length = (end_date - start_date).days + 1
        prev_start = start_date - timedelta(days=period_length)
        prev_end = start_date - timedelta(days=1)

    except ValueError:
        st.sidebar.warning("Por favor selecciona un rango válido de fechas (inicio y fin).")
        st.write("Esperando selección de rango de fechas...")
        return

    # ////////////////// Resources ///////////////////////
    df_muscles_filtered = filter_by_date(df_muscles, start_date, end_date)
    df_muscles_prev = filter_by_date(df_muscles, prev_start, prev_end)

    metrics = {
        'Series Directas': ('series_principal','sum'), 
        'Total Series': ('series_counter','sum'),
        'Series Efectivas': ('effective_set_counter','sum'),
        'Workload': ('workload_real','sum'),
        }
    
    df_processed = calculate_summary_table(
                                        df_now=df_muscles_filtered, 
                                        df_prev=df_muscles_prev, 
                                        group_col="id_muscle",
                                        metrics=metrics
                                        )
    
    prev_cols = [col for col in df_processed.columns if "_prev" in col]
    df_processed.drop(columns=prev_cols, inplace=True)
    df_processed = compute_difference_between_kpis(df_processed, 'Series Efectivas', 'Total Series')

    table_1_metrics = ['id_muscle'] + [col for col in df_processed.columns if any(word in col.lower() for word in ['directas', 'total'])]
    table_1_metrics = reorder_columns(table_1_metrics)
    table_1_metrics.remove('Series Efectivas_vs_Total Series')
    table_2_metrics = ['id_muscle'] + [col for col in df_processed.columns if any(word in col.lower() for word in ['efectivas', 'total'])]
    table_2_metrics = reorder_columns(table_2_metrics)
    table_2_metrics = [col for col in table_2_metrics if col not in ['Series Efectivas_vs_Total Series','%_series_efectivas','Δ_%_series_efectivas']]
    table_3_metrics = ['id_muscle'] + [col for col in df_processed.columns if any(word in col.lower() for word in ['workload'])]
    table_3_metrics = reorder_columns(table_3_metrics)
    # ////////////////// Display //////////////////////////
    st.markdown(
        f"""
        <div style='color: rgba(213, 212, 213,0.5); font-size: 0.9rem;'>
            <strong>Periodo seleccionado:</strong> {start_date.strftime('%d %b %Y')} — {end_date.strftime('%d %b %Y')} ({period_length} días)
            <br>
            <strong>Comparando con:</strong> {prev_start.strftime('%d %b %Y')} — {prev_end.strftime('%d %b %Y')}
        </div>
        """,
        unsafe_allow_html=True
    )
    # Section 1: Direct sets and total sets
    st.subheader("💪 Análisis de series directas y totales")
    # Tabla 1
    display_summary_table(
                        df_processed[table_1_metrics],
                        group_col="id_muscle",
                        title="Resumen por ejercicio (actual vs anterior)"
                        )
    
    # Section 2: Effective sets and total sets
    st.subheader("💪 Análisis de series efectivas y totales")
    plot_muscle_analysis(
        data=df_processed,
        x1_col="Series Efectivas",
        x2_col="Series Efectivas_vs_Total Series",
        y_col="id_muscle",
        x1_label="Series Efectivas",
        x2_label="Total Series",
        custom_data_labels=['%_series_efectivas', None],
        x1_suffix="%",
        title="Muscle Analysis",
        hide_xaxis=True,
    )

    # Tabla 2
    display_summary_table(
                        df_processed[table_2_metrics],
                        group_col="id_muscle",
                        title="Resumen por ejercicio (actual vs anterior)"
                        )
    
    # Section 3: Workload
    st.subheader("💪 Análisis de carga de trabajo")

    plot_muscle_analysis(
        data=df_processed,
        x1_col="Δ_Workload",
        y_col="id_muscle",
        x1_label="Δ_Workload",
        title="Muscle Analysis",
        x1_suffix="%",
        hide_xaxis=True,
        data_prefix=[True, False]
    )

    # Tabla 3
    display_summary_table(
                        df_processed[table_3_metrics],
                        group_col="id_muscle",
                        title="Resumen por ejercicio (actual vs anterior)"
                        )
    
if __name__ == "__main__":
    main()