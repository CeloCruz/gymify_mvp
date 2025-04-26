import sqlite3
import os
import pandas as pd
from pathlib import Path

def create_database():
    """Create SQLite database and tables if they don't exist"""
    # Use absolute path for Streamlit Cloud compatibility
    db_dir = Path(__file__).parent
    db_path = db_dir / "fitness_tracker.db"

    # Ensure the database directory exists
    db_dir.mkdir(parents=True, exist_ok=True)

    # Connect to database (will create if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table for authentication
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create workouts table (replaces track_record_aggregated.csv)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATE NOT NULL,
        fecha_prev DATE,
        fecha_next DATE,
        exercise TEXT NOT NULL,
        routine TEXT NOT NULL,
        reprange TEXT,
        repreal INTEGER,
        weight REAL,
        rir INTEGER,
        workload_total REAL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create muscle_breakdown table (replaces track_record_breakdown_muscles.csv)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS muscle_breakdown (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATE NOT NULL,
        fecha_prev DATE,
        fecha_next DATE,
        exercise TEXT NOT NULL,
        id_muscle TEXT NOT NULL,
        id_rol TEXT NOT NULL,
        workload REAL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create routine_templates table (replaces Fitness Personal - Routines.csv)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS routine_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        routine TEXT NOT NULL,
        exercise TEXT NOT NULL,
        rep_t_min INTEGER,
        rep_t_max INTEGER,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create exercise_muscles table (replaces TrackRecord - MuscleRoles.csv)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercise_muscles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_exercise TEXT NOT NULL,
        id_pattern TEXT,
        id_muscle TEXT NOT NULL,
        id_rol TEXT NOT NULL,
        english_name TEXT
    )
    ''')

    conn.commit()
    conn.close()

    print("Database and tables created successfully")

def import_csv_data():
    """Import data from CSV files into SQLite database"""
    # Use absolute path for Streamlit Cloud compatibility
    db_dir = Path(__file__).parent
    db_path = db_dir / "fitness_tracker.db"

    # Get connection to database
    conn = sqlite3.connect(db_path)

    # Get the root directory (project root)
    root_dir = Path(__file__).parent.parent
    data_dir = root_dir / "data"

    # Import aggregated workout data
    try:
        agg_path = data_dir / "20250405_track_record_aggregated.csv"
        df_agg = pd.read_csv(agg_path, parse_dates=['fecha', 'fecha_prev', 'fecha_next'])
        # Convert dates to string format for SQLite
        for col in ['fecha', 'fecha_prev', 'fecha_next']:
            df_agg[col] = df_agg[col].dt.strftime('%Y-%m-%d')
        # Add user_id column (default to admin user with ID 1)
        if 'user_id' not in df_agg.columns:
            df_agg['user_id'] = 1
        df_agg.to_sql('workouts', conn, if_exists='replace', index=False)
        print("Imported aggregated workout data")
    except Exception as e:
        print(f"Error importing aggregated data: {e}")

    # Import muscle breakdown data
    try:
        muscles_path = data_dir / "20250405_track_record_breakdown_muscles.csv"
        df_muscles = pd.read_csv(muscles_path, parse_dates=['fecha', 'fecha_prev', 'fecha_next'])
        # Convert dates to string format for SQLite
        for col in ['fecha', 'fecha_prev', 'fecha_next']:
            df_muscles[col] = df_muscles[col].dt.strftime('%Y-%m-%d')
        # Add user_id column (default to admin user with ID 1)
        if 'user_id' not in df_muscles.columns:
            df_muscles['user_id'] = 1
        df_muscles.to_sql('muscle_breakdown', conn, if_exists='replace', index=False)
        print("Imported muscle breakdown data")
    except Exception as e:
        print(f"Error importing muscle breakdown data: {e}")

    # Import routine templates
    try:
        routines_path = data_dir / "Fitness Personal - Routines.csv"
        df_routines = pd.read_csv(routines_path)
        # Convert column names to snake_case
        df_routines.columns = df_routines.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
        # Add user_id column (default to admin user with ID 1)
        if 'user_id' not in df_routines.columns:
            df_routines['user_id'] = 1
        df_routines.to_sql('routine_templates', conn, if_exists='replace', index=False)
        print("Imported routine templates")
    except Exception as e:
        print(f"Error importing routine templates: {e}")

    # Import exercise muscles data
    try:
        muscles_roles_path = data_dir / "TrackRecord - MuscleRoles.csv"
        df_ex_muscles = pd.read_csv(muscles_roles_path)
        df_ex_muscles.to_sql('exercise_muscles', conn, if_exists='replace', index=False)
        print("Imported exercise muscles data")
    except Exception as e:
        print(f"Error importing exercise muscles data: {e}")

    conn.close()

if __name__ == "__main__":
    create_database()
    import_csv_data()
