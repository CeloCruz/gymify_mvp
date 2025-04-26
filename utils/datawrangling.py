import pandas as pd
import numpy as np
import streamlit as st

def filter_by_routine(df, routine, routine_col="routine"):
    """
    Filters a DataFrame to return only rows matching the selected routine.
    Raises an error if the column is missing, returns empty if routine not found.
    """
    if routine_col not in df.columns:
        raise KeyError(f"Column '{routine_col}' not found in DataFrame.")
    if routine not in df[routine_col].values:
        st.warning(f"Routine '{routine}' not found in column '{routine_col}'. Returning empty DataFrame.")
        return df.iloc[0:0].copy()
    return df[df[routine_col] == routine].copy()

def order_historial(df):
    """
    Orders a DataFrame by 'fecha' descending and 'id_serie' ascending if present.
    Returns the original DataFrame if those columns are missing or DataFrame is empty.
    """
    if df.empty:
        return df

    sort_cols = []
    ascending = []

    if "fecha" in df.columns:
        sort_cols.append("fecha")
        ascending.append(False)
    if "id_serie" in df.columns:
        sort_cols.append("id_serie")
        ascending.append(True)

    if not sort_cols:
        st.warning("No columns found for ordering. Returning original DataFrame.")
        return df

    return df.sort_values(by=sort_cols, ascending=ascending)

def rep_concatenate(df, repmin_col: str = "repmin", repmax_col: str = "repmax"):
    """
    Combines min and max rep values into a single 'reprange' column for readability.
    Handles Myo/Dropset tags and gracefully deals with missing or malformed data.
    Drops original columns after processing.
    """
    if repmin_col not in df.columns or repmax_col not in df.columns:
        st.warning(f"Columns '{repmin_col}' or '{repmax_col}' not found. Returning DataFrame unchanged.")
        return df

    def format_number(x):
        try:
            x_float = float(x)
            return str(int(x_float)) if x_float == int(x_float) else str(x_float)
        except (ValueError, TypeError):
            return str(x) if pd.notna(x) else ""

    try:
        df["reprange"] = np.where(
            df[repmin_col].isin(['Myo', 'Dropset']),
            df[repmin_col],
            np.where(
                (df[repmin_col] != -1) & (df[repmax_col].notnull()),
                df[repmin_col].apply(format_number) + " - " + df[repmax_col].apply(format_number),
                np.where(df[repmin_col].isnull(), df[repmin_col], 'Dropset')
            )
        )
        df.drop(columns=[repmin_col, repmax_col], inplace=True)
    except Exception as e:
        st.error(f"Error concatenating rep range: {e}")
    return df

def preprocess_routine_history(df: pd.DataFrame) -> pd.DataFrame:
    df = order_historial(df)
    df = rep_concatenate(df)
    return df