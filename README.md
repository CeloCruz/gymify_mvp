# Fitness Dashboard

A Streamlit dashboard for tracking workout progress with authentication and SQLite database.

## Features

- User authentication system
- SQLite database for data storage
- Multiple dashboard views:
  - Overview with KPIs
  - Progress tracking
  - Muscle analysis
  - Workout history
  - Routine templates
- Mobile-responsive design

## Setup and Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run home.py
   ```

## First-time Setup

1. When you first run the application, a SQLite database will be created
2. Log in with the default admin account:
   - Username: `admin`
   - Password: `admin123`
3. Use the admin panel to import your CSV data into the SQLite database

## Deploying to Streamlit Cloud

1. Push your code to a GitHub repository
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your GitHub repository
4. Set the main file to `home.py`
5. Deploy the app

## Database Structure

The application uses SQLite with the following tables:

- `users`: User authentication data
- `workouts`: Main workout tracking data
- `muscle_breakdown`: Muscle-specific workout data
- `routine_templates`: Workout routine templates
- `exercise_muscles`: Exercise to muscle mappings

## Authentication

The app uses `streamlit-authenticator` for user management. New users can sign up through the login page.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
