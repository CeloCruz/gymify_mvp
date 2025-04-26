import pandas as pd

def simple_locale_format(val, fmt="{:,.0f}"):
    # First, format the value using the standard formatter:
    formatted = fmt.format(val)
    # Then swap commas and periods using a temporary placeholder.
    return formatted.replace(",", "TMP").replace(".", ",").replace("TMP", ".")

def format_fecha_column(df: pd.DataFrame, col_fecha: str, granularity: str) -> pd.DataFrame:
    """
    Formats the 'fecha' column in df based on the time granularity.
    """
    if 'fecha' not in df.columns:
        raise ValueError("'fecha' column is required.")

    # Ensure it's datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    if granularity in ['D', 'day']:
        df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
    elif granularity in ['W', 'week']:
        df['fecha'] = df['fecha'].dt.strftime('%G-W%V')
    elif granularity in ['M', 'month']:
        df['fecha'] = df['fecha'].dt.strftime('%Y-%m')
    else:
        # fallback to ISO format if unknown granularity
        df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return df
