"""
prompt_builder.py

Builds the prompt that is sent to Google Gemini.
"""

def build_prompt(schema: str, user_question: str) -> str:
    """
    Creates a prompt for Gemini to generate PostgreSQL SQL.

    Parameters
    ----------
    schema : str
        Database schema loaded dynamically.

    user_question : str
        Natural language question entered by the user.

    Returns
    -------
    str
        Prompt to send to Gemini.
    """

    prompt = f"""
You are an expert PostgreSQL SQL developer.

Your task is to generate a valid PostgreSQL SQL query based on the database schema and the user's question.

=========================
DATABASE SCHEMA
=========================

{schema}

=========================
USER QUESTION
=========================

{user_question}

=========================
IMPORTANT RULES
=========================

1. Generate ONLY PostgreSQL SQL.
2. Do NOT generate explanations.
3. Do NOT generate markdown.
4. Do NOT generate comments.
5. Return ONLY the SQL query.
6. Use only the tables and columns available in the schema.
7. If multiple tables are needed, use the appropriate JOIN based on the foreign key relationships.
8. Do not invent table names or column names.
9. The SQL must be executable in PostgreSQL.

SQL:
"""

    return prompt