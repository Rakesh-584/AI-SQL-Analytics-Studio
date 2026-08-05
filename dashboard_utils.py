"""
dashboard_utils.py

Functions for collecting dashboard statistics
from PostgreSQL.
"""

import pandas as pd
from sqlalchemy import text

from database import get_engine
from config import DATABASE_NAME


# ---------------------------------------------
# Dashboard KPIs
# ---------------------------------------------

def get_dashboard_stats():
    """
    Returns:
        - Database Name
        - Total Tables
        - Total Rows
        - Total Columns
    """

    engine = get_engine()

    # -----------------------------
    # Get all tables
    # -----------------------------

    tables_query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    ORDER BY table_name;
    """

    tables = pd.read_sql(
        text(tables_query),
        engine
    )

    total_tables = len(tables)

    total_rows = 0
    total_columns = 0

    table_summary = []

    # -----------------------------
    # Loop through every table
    # -----------------------------

    for table in tables["table_name"]:

        # Row Count
        rows = pd.read_sql(
            text(f"SELECT COUNT(*) AS total FROM {table}"),
            engine
        ).iloc[0]["total"]

        # Column Count
        cols = pd.read_sql(
            text(f"""
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_name='{table}'
            """),
            engine
        ).iloc[0][0]

        total_rows += rows
        total_columns += cols

        table_summary.append({
            "Table": table,
            "Rows": rows,
            "Columns": cols
        })

    return {
        "database": DATABASE_NAME,
        "tables": total_tables,
        "rows": total_rows,
        "columns": total_columns,
        "summary": pd.DataFrame(table_summary)
    }