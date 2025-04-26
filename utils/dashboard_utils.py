import streamlit as st
from datetime import timedelta
from utils.data_loader import load_data, filter_by_date, get_date_filters

def load_common_resources(filepath_agg: str, filepath_muscles: str) -> dict:
    """Centralized loading and filtering logic for dashboard pages."""
    df, df_muscles = load_data(filepath_agg, filepath_muscles)

    min_date, max_date = get_date_filters(df)
    start_date, end_date = st.sidebar.date_input(
        "Rango de fechas",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    period_length = (end_date - start_date).days + 1
    prev_start = start_date - timedelta(days=period_length)
    prev_end = start_date - timedelta(days=1)

    df_filtered = filter_by_date(df, start_date, end_date)
    df_prev = filter_by_date(df, prev_start, prev_end)
    df_muscles_filtered = filter_by_date(df_muscles, start_date, end_date)
    df_muscles_prev = filter_by_date(df_muscles, prev_start, prev_end)

    return {
        "df": df,
        "df_muscles": df_muscles,
        "df_filtered": df_filtered,
        "df_prev": df_prev,
        "df_muscles_filtered": df_muscles_filtered,
        "df_muscles_prev": df_muscles_prev,
        "start_date": start_date,
        "end_date": end_date,
        "prev_start": prev_start,
        "prev_end": prev_end,
        "period_length": period_length
    }
