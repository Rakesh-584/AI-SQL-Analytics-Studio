"""
export_utils.py

Professional Export Center
"""

import streamlit as st
import pandas as pd

from report_generator import (
    create_pdf_report,
    create_excel_report
)


def show_export_buttons(
        df,
        sql_query,
        question):

    st.subheader("📥 Export Results")

    fig = st.session_state.get(
        "current_chart",
        None
    )

    col1, col2, col3, col4 = st.columns(4)

    # -----------------------------
    # CSV
    # -----------------------------

    with col1:

        st.download_button(

            "📄 CSV",

            df.to_csv(index=False),

            "query_results.csv",

            "text/csv"

        )

    # -----------------------------
    # JSON
    # -----------------------------

    with col2:

        st.download_button(

            "📑 JSON",

            df.to_json(
                orient="records",
                indent=4
            ),

            "query_results.json",

            "application/json"

        )

    # -----------------------------
    # Excel
    # -----------------------------

    with col3:

        excel = create_excel_report(
            df,
            fig,
            sql_query,
            question
        )

        st.download_button(

            "📊 Excel Report",

            excel,

            "AI_SQL_Report.xlsx",

            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )

    # -----------------------------
    # PDF
    # -----------------------------

    with col4:

        pdf = create_pdf_report(
            df,
            fig,
            sql_query,
            question
        )

        st.download_button(

            "📕 PDF Report",

            pdf,

            "AI_SQL_Report.pdf",

            "application/pdf"

        )