"""
schema_loader.py

Loads the PostgreSQL database schema dynamically.
No table names or column names are hardcoded.
"""

import pandas as pd
from sqlalchemy import text

from database import get_engine
from config import DB_NAME


def load_database_schema():
    """
    Fetches database schema dynamically.

    Returns
    -------
    str
        Formatted schema description for Gemini.
    """

    engine = get_engine()

    schema_text = []
    schema_text.append(f"Database: {DB_NAME}")
    schema_text.append("=" * 60)

    with engine.connect() as connection:

        # ----------------------------------------
        # Fetch all tables
        # ----------------------------------------

        tables_query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        ORDER BY table_name;
        """

        tables = pd.read_sql(text(tables_query), connection)

        for table in tables["table_name"]:

            schema_text.append(f"\nTable: {table}")

            # ----------------------------------------
            # Fetch columns
            # ----------------------------------------

            columns_query = f"""
            SELECT
                column_name,
                data_type
            FROM information_schema.columns
            WHERE table_name='{table}'
            ORDER BY ordinal_position;
            """

            columns = pd.read_sql(text(columns_query), connection)

            schema_text.append("Columns:")

            for _, row in columns.iterrows():
                schema_text.append(
                    f"   - {row['column_name']} ({row['data_type']})"
                )

            # ----------------------------------------
            # Primary Keys
            # ----------------------------------------

            pk_query = f"""
            SELECT
                kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            WHERE tc.constraint_type='PRIMARY KEY'
            AND tc.table_name='{table}';
            """

            pk = pd.read_sql(text(pk_query), connection)

            if not pk.empty:
                schema_text.append("Primary Keys:")

                for col in pk["column_name"]:
                    schema_text.append(f"   - {col}")

            # ----------------------------------------
            # Foreign Keys
            # ----------------------------------------

            fk_query = f"""
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table,
                ccu.column_name AS foreign_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type='FOREIGN KEY'
            AND tc.table_name='{table}';
            """

            fk = pd.read_sql(text(fk_query), connection)

            if not fk.empty:

                schema_text.append("Foreign Keys:")

                for _, row in fk.iterrows():

                    schema_text.append(
                        f"   - {row['column_name']} -> "
                        f"{row['foreign_table']}."
                        f"{row['foreign_column']}"
                    )

    return "\n".join(schema_text)