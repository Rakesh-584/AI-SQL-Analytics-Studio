"""
config.py

Stores PostgreSQL database configuration.
The Gemini API Key will be entered by the user
through the Streamlit application.
"""

# ----------------------------------------
# PostgreSQL Configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_NAME = "Ecommerce"

DB_PASSWORD = None
# ----------------------------------------



GEMINI_MODEL = "models/gemini-3.6-flash"

def get_database_url():
    """
    Returns the SQLAlchemy PostgreSQL connection URL.
    """
    return (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )