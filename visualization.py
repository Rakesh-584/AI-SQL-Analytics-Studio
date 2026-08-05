"""
visualization.py

Interactive visualization using Plotly.
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def show_visualization(df: pd.DataFrame):

    if df.empty:
        st.info("No data available for visualization.")
        return

    st.subheader("📊 Visualization Studio")

    # -----------------------------
    # Chart Type
    # -----------------------------

    chart_type = st.selectbox(
        "Select Chart",
        [
            "Bar Chart",
            "Line Chart",
            "Area Chart",
            "Scatter Plot",
            "Pie Chart"
        ],
        key="chart_type"
    )

    # -----------------------------
    # Columns
    # -----------------------------

    columns = df.columns.tolist()

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if len(columns) < 2:
        st.warning("Need at least two columns.")
        return

    if len(numeric_columns) == 0:
        st.warning("No numeric columns available.")
        return

    # -----------------------------
    # X Axis
    # -----------------------------

    x_axis = st.selectbox(
        "X-Axis",
        columns,
        key="x_axis"
    )

    # -----------------------------
    # Y Axis
    # -----------------------------

    available_y = [col for col in numeric_columns if col != x_axis]

    if not available_y:
        available_y = numeric_columns

    y_axis = st.selectbox(
        "Y-Axis",
        available_y,
        key="y_axis"
    )

    # -----------------------------
    # Bar Chart
    # -----------------------------

    if chart_type == "Bar Chart":

        fig = px.bar(
            df,
            x=x_axis,
            y=y_axis,
            text_auto=True,
            title=f"{y_axis} by {x_axis}"
        )
        st.session_state["current_chart"] = fig
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Line Chart
    # -----------------------------

    elif chart_type == "Line Chart":

        fig = px.line(
            df,
            x=x_axis,
            y=y_axis,
            markers=True,
            title=f"{y_axis} by {x_axis}"
        )
        st.session_state["current_chart"] = fig
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Area Chart
    # -----------------------------

    elif chart_type == "Area Chart":

        fig = px.area(
            df,
            x=x_axis,
            y=y_axis,
            title=f"{y_axis} by {x_axis}"
        )
        st.session_state["current_chart"] = fig
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Scatter Plot
    # -----------------------------

    elif chart_type == "Scatter Plot":

        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            size=y_axis,
            hover_data=columns,
            title=f"{y_axis} vs {x_axis}"
        )
        st.session_state["current_chart"] = fig
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Pie Chart
    # -----------------------------

    elif chart_type == "Pie Chart":

        fig = px.pie(
            df,
            names=x_axis,
            values=y_axis,
            hole=0.4,
            title=f"{y_axis} Distribution"
        )
        st.session_state["current_chart"] = fig
        st.plotly_chart(
            fig,
            use_container_width=True
        )