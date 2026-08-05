"""
database_browser.py

Displays all database tables and columns
in the Streamlit sidebar.
"""

import pandas as pd
from sqlalchemy import text

from database import get_engine


def get_database_structure():
    """
    Returns a dictionary containing
    all tables and columns.
    """

    engine = get_engine()

    query = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema='public'
    ORDER BY table_name,
             ordinal_position;
    """

    with engine.connect() as conn:

        df = pd.read_sql(
            text(query),
            conn
        )

    tables = {}

    for table in df["table_name"].unique():

        table_df = df[
            df["table_name"] == table
        ]

        tables[table] = list(
            zip(
                table_df["column_name"],
                table_df["data_type"]
            )
        )

    return tables