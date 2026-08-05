"""
database.py

Handles PostgreSQL database connection
and SQL query execution.
"""

import streamlit as st
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_NAME
)


# ----------------------------------------
# Create SQLAlchemy Engine
# ----------------------------------------

def get_engine():

    password = st.session_state.get("db_password", "")

    connection_url = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{password}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return create_engine(connection_url)


# ----------------------------------------
# Test Database Connection
# ----------------------------------------

def test_connection():

    password = st.session_state.get("db_password", "")

    if password == "":
        return False, "Please enter the PostgreSQL password."

    try:

        engine = get_engine()

        with engine.connect():
            pass

        return True, "✅ Database connected successfully."

    except SQLAlchemyError as e:

        return False, str(e)


# ----------------------------------------
# Execute SQL Query
# ----------------------------------------

def execute_query(query):

    try:

        engine = get_engine()

        with engine.connect() as connection:

            df = pd.read_sql(
                text(query),
                connection
            )

        return df

    except SQLAlchemyError as e:

        raise Exception(f"Database Error:\n{e}")

    except Exception as e:

        raise Exception(f"Unexpected Error:\n{e}")