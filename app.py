"""
app.py

Main Streamlit application for AI-powered Text-to-SQL.
"""

import streamlit as st
import pandas as pd
from sqlalchemy import text
import plotly.express as px

from export_utils import show_export_buttons
from database import (test_connection,execute_query,get_engine)
from schema_loader import load_database_schema
from prompt_builder import build_prompt
from gemini_service import configure_gemini, generate_sql
from visualization import show_visualization

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI SQL Analytics Studio",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI SQL Analytics Studio")
st.caption("Analyze your PostgreSQL database using Natural Language and Google Gemini.")

st.divider()
# -------------------------------------------------
# Session State
# -------------------------------------------------

if "sql_query" not in st.session_state:
    st.session_state.sql_query = None

if "query_result" not in st.session_state:
    st.session_state.query_result = None

if "user_question" not in st.session_state:
    st.session_state.user_question = ""
# -------------------------------------------------
# Tabs
# -------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🤖 AI Query",
        "🗄 Tables",
        "📊 Dashboard",
        "⚙ Settings"
    ]
)

# =================================================
# AI QUERY TAB
# =================================================

# =================================================
# AI QUERY TAB
# =================================================

with tab1:

    # ---------------------------------------------
    # Gemini API Key
    # ---------------------------------------------

    # ---------------------------------------------
# Database Password
# ---------------------------------------------

    db_password = st.text_input(
        "🔐 Enter PostgreSQL Password",
        type="password"
)

    if db_password:
        st.session_state.db_password = db_password
    
    st.caption(
    "Enter your local PostgreSQL password. "
    "The password is used only for this session and is not stored."
)

# ---------------------------------------------
# Gemini API Key
# ---------------------------------------------

    api_key = st.text_input(
        "🤖 Enter your Gemini API Key",
        type="password"
)

    # ---------------------------------------------
    # Database Connection
    # ---------------------------------------------

    success, message = test_connection()

    if success:
        st.success(message)
    else:
        st.error(message)
        st.stop()

    # ---------------------------------------------
    # Load Database Schema
    # ---------------------------------------------

    try:

        schema = load_database_schema()

        with st.expander("📂 View Database Schema"):
            st.text(schema)

    except Exception as e:

        st.error(f"Schema Loading Error:\n{e}")
        st.stop()

    # ---------------------------------------------
    # User Question
    # ---------------------------------------------

    question = st.text_area(
        "Ask a question about your database",
        value=st.session_state.user_question,
        placeholder="Example: Show all customers from Hyderabad."
    )

    # ---------------------------------------------
    # Buttons
    # ---------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        generate = st.button(
            "🚀 Generate SQL",
            use_container_width=True
        )

    with col2:

        clear = st.button(
            "🗑 New Query",
            use_container_width=True
        )

    # ---------------------------------------------
    # Clear Session
    # ---------------------------------------------

    if clear:

        st.session_state.sql_query = None
        st.session_state.query_result = None
        st.session_state.user_question = ""

        st.rerun()

    # ---------------------------------------------
    # Generate SQL
    # ---------------------------------------------

    if generate:

        if not api_key:

            st.warning("Please enter your Gemini API Key.")
            st.stop()

        if not question.strip():

            st.warning("Please enter a question.")
            st.stop()

        try:

            # Configure Gemini
            configure_gemini(api_key)

            # Build Prompt
            prompt = build_prompt(
                schema,
                question
            )

            # Generate SQL
            sql_query = generate_sql(prompt)

            # Execute SQL
            df = execute_query(sql_query)

            # Save Results
            st.session_state.sql_query = sql_query
            st.session_state.query_result = df
            st.session_state.user_question = question

        except Exception as e:

            st.error(str(e))

    # ---------------------------------------------
    # Display Results
    # ---------------------------------------------

    if st.session_state.query_result is not None:

        st.divider()

        st.subheader("📝 Generated SQL")

        st.code(
            st.session_state.sql_query,
            language="sql"
        )

        st.subheader("📋 Query Results")

        st.dataframe(
            st.session_state.query_result,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        show_visualization(
            st.session_state.query_result
        )

        st.divider()

        show_export_buttons(
        st.session_state.query_result,
        st.session_state.sql_query,
        st.session_state.user_question
        )

# =================================================
# TABLES TAB
# =================================================

# =================================================
# TABLES TAB
# =================================================

# =================================================
# TABLES TAB
# =================================================

with tab2:

    st.header("🗄 Database Tables")

    engine = get_engine()

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

    table_list = tables["table_name"].tolist()

    if len(table_list) == 0:

        st.warning("No tables found.")

    else:

        selected_table = st.selectbox(
            "Select Table",
            table_list
        )

        # --------------------------
        # Row Count
        # --------------------------

        row_count = pd.read_sql(
            text(f"SELECT COUNT(*) AS total FROM {selected_table}"),
            engine
        ).iloc[0]["total"]

        # --------------------------
        # Columns
        # --------------------------

        columns_query = f"""
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_name='{selected_table}'
        ORDER BY ordinal_position;
        """

        columns = pd.read_sql(
            text(columns_query),
            engine
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", row_count)

        with col2:
            st.metric("Columns", len(columns))

        st.subheader("📋 Columns")

        st.dataframe(
            columns,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------
        # Preview
        # --------------------------

        preview = pd.read_sql(
            text(f"SELECT * FROM {selected_table} LIMIT 20"),
            engine
        )

        st.subheader("👀 Preview")

        st.dataframe(
            preview,
            use_container_width=True,
            hide_index=True
        )
# =================================================
# DASHBOARD TAB
# =================================================

with tab3:

    st.header("📊 Database Dashboard")

    engine = get_engine()

    # ---------------------------------
    # Total Tables
    # ---------------------------------

    total_tables = pd.read_sql(
        text("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema='public'
        """),
        engine
    ).iloc[0, 0]

    # ---------------------------------
    # Database Name
    # ---------------------------------

    database_name = pd.read_sql(
        text("SELECT current_database();"),
        engine
    ).iloc[0, 0]

    # ---------------------------------
    # Total Columns
    # ---------------------------------

    total_columns = pd.read_sql(
        text("""
        SELECT COUNT(*)
        FROM information_schema.columns
        WHERE table_schema='public'
        """),
        engine
    ).iloc[0, 0]

    # ---------------------------------
    # Total Rows
    # ---------------------------------

    total_rows = 0

    table_names = pd.read_sql(
        text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        """),
        engine
    )

    rows_data = []

    for table in table_names["table_name"]:

        rows = pd.read_sql(
            text(f"SELECT COUNT(*) FROM {table}"),
            engine
        ).iloc[0, 0]

        total_rows += rows

        rows_data.append(
            {
                "Table": table,
                "Rows": rows
            }
        )

    rows_df = pd.DataFrame(rows_data)

    # ---------------------------------
    # KPI Cards
    # ---------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🗄 Tables", total_tables)
    c2.metric("📄 Rows", f"{total_rows:,}")
    c3.metric("📑 Columns", total_columns)
    c4.metric("💾 Database", database_name)

    st.divider()

    # ---------------------------------
    # Charts
    # ---------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Rows per Table")

        st.bar_chart(
            rows_df.set_index("Table")
        )

    with col2:

        st.subheader("Table Distribution")

        st.plotly_chart(
            px.pie(
                rows_df,
                names="Table",
                values="Rows",
                hole=0.4
            ),
            use_container_width=True
        )

    st.divider()

    st.subheader("📋 Table Statistics")

    st.dataframe(
        rows_df,
        use_container_width=True,
        hide_index=True
    )

# =================================================
# SETTINGS TAB
# =================================================

with tab4:

    st.header("⚙ Application Settings")

    st.subheader("🤖 AI Configuration")

    st.success("Gemini API Connected")

    st.write("Current Model")

    st.code("gemini-3.6-flash")

    st.divider()

    st.subheader("🗄 Database")

    db_name = pd.read_sql(
        text("SELECT current_database();"),
        get_engine()
    ).iloc[0, 0]

    db_version = pd.read_sql(
        text("SELECT version();"),
        get_engine()
    ).iloc[0, 0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Database",
            db_name
        )

    with col2:
        st.metric(
            "Status",
            "Connected ✅"
        )

    with st.expander("PostgreSQL Version"):

        st.write(db_version)

    st.divider()

    st.subheader("📂 Schema")

    if st.button(
        "🔄 Refresh Database Schema",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.success("Database schema refreshed successfully.")

    st.divider()

    st.subheader("🧹 Session")

    if st.button(
        "🗑 Clear Current Query",
        use_container_width=True
    ):

        st.session_state.sql_query = None
        st.session_state.query_result = None
        st.session_state.user_question = ""

        st.success("Current query cleared.")

    st.divider()

    st.subheader("ℹ About")

    st.info(
        """
### AI SQL Analytics Studio

Version : 2.0

Developer : Rakesh Gunti

Features

✅ AI Text-to-SQL

✅ PostgreSQL Integration

✅ Interactive Dashboard

✅ Database Explorer

✅ Data Visualization

✅ Export to CSV

✅ Export to Excel

✅ Export to JSON

✅ Export to PDF
"""
    )