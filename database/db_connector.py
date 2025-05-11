import sqlite3
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import pymysql

# ///////////////////// MySQL Database Connection ////////////////////
def get_db_connection():
    """Get a SQLAlchemy engine connection to the MySQL database"""
    # Parámetros de conexión
    engine = create_engine("mysql+pymysql://admin:Macs.991014.@localhost/fitnessdb")
    conn = engine.connect()
    return conn

def execute_query(query, params=(), fetchall=True):
    """Execute a query and return results (MySQL-compatible)"""
    conn = get_db_connection()
    result = conn.execute(query, params)

    if fetchall:
        results = result.fetchall()
    else:
        conn.commit()
        results = None

    conn.close()
    return results

def query_to_dataframe(query, params=()):
    """Execute a query and return results as a pandas DataFrame"""
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# //////////////////// SQLite Database Connection ////////////////////
def get_db_connection():
    """Get a connection to the SQLite database"""
    # Use absolute path for Streamlit Cloud compatibility
    db_dir = Path(__file__).parent
    db_path = db_dir / "fitness_tracker.db"

    # Create directory if it doesn't exist
    db_dir.mkdir(parents=True, exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def execute_query(query, params=(), fetchall=True):
    """Execute a query and return results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)

    if fetchall:
        results = cursor.fetchall()
    else:
        conn.commit()
        results = None

    conn.close()
    return results

def query_to_dataframe(query, params=()):
    """Execute a query and return results as a pandas DataFrame"""
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def insert_data(table, data_dict):
    """Insert a row of data into a table"""
    conn = get_db_connection()
    cursor = conn.cursor()

    columns = ', '.join(data_dict.keys())
    placeholders = ', '.join(['?' for _ in data_dict])
    values = tuple(data_dict.values())

    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, values)

    last_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return last_id

def update_data(table, data_dict, condition_dict):
    """Update rows in a table that match the condition"""
    conn = get_db_connection()
    cursor = conn.cursor()

    set_clause = ', '.join([f"{key} = ?" for key in data_dict.keys()])
    where_clause = ' AND '.join([f"{key} = ?" for key in condition_dict.keys()])

    values = list(data_dict.values()) + list(condition_dict.values())

    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    cursor.execute(query, values)

    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    return rows_affected
