from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import streamlit as st
import os
import sqlite3
from google import genai

def init_db():
    con = sqlite3.connect("student.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS student (
            name TEXT,
            dept TEXT,
            section TEXT,
            marks INTEGER
        );
    """)

    cur.execute("SELECT COUNT(*) FROM student")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO student VALUES (?, ?, ?, ?)",
            [
                ('Abbas Mirza','IT','2',92),
                ('Tharun','IT','2',80),
                ('Tarun','IT','2',90),
                ('Rohan','IT','2',74),
                ('Anurag','IT','2',89),
                ('Nishant','IT','2',83)
            ]
        )

    con.commit()
    con.close()

init_db()

# ---------- GEMINI ----------
def get_gemini_res(question, prompt):
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options={"api_version": "v1"}
    )

    full_prompt = prompt[0] + "\nQuestion: " + question

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return response.text.strip()

# ---------- SQL ----------
def read_sql_query(sql, db):
    # Basic safety check
    if not "select" in sql.lower():
        return "Only SELECT queries are allowed."
    if ";" in sql.strip()[:-1]:
        return "Multiple SQL statements are not allowed."
    dangerous = ["drop", "delete", "update", "insert", "alter", "create"]

    if any(word in sql.lower() for word in dangerous):
        return "Destructive operations are not allowed."
    con=sqlite3.connect("file:student.db?mode=ro", uri=True)
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cols=[desc[0] for desc in cur.description]
    con.close()
    return pd.DataFrame(rows,columns=cols)


# ---------- PROMPT ----------
prompt = ["""
You are an AI system that converts administrator requests into safe SQL queries.

The database table is named STUDENT with columns:
- NAME (TEXT)
- DEPT (TEXT)
- SECTION (TEXT)
- MARKS (INTEGER)

Rules:
- Generate ONLY a single valid SQL SELECT query.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or any destructive operations.
- If the user asks to delete, modify, or update data, instead generate a SELECT query that shows which records would be affected.
- Use case-insensitive matching when filtering text fields.
- Use LIKE with wildcards (%) when appropriate for partial matches.
- Do not include explanations or markdown formatting.
- Output only raw SQL.

Examples:
User: What are the marks of Abbas?
SQL: SELECT NAME, MARKS FROM STUDENT WHERE LOWER(NAME) LIKE LOWER('%abbas%');

User: Remove Abbas from the table.
SQL: SELECT * FROM STUDENT WHERE LOWER(NAME) LIKE LOWER('%abbas%');
"""
]

# ---------- UI ----------
st.set_page_config(page_title="SQLens", page_icon="🔍")

st.markdown("""
<style>
.stButton>button {
    background-color: #00f5d4;
    color: black;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
col1, col2 = st.columns([1, 4])

with col1:
    # Display your logo
    st.image("logo.png", width=200)

with col2:
    # 2. Use HTML <marquee> for the scrolling effect
    # We use st.markdown with unsafe_allow_html=True to render the custom HTML
    scrolling_text_html = """
        <div style="display: flex; align-items: center; height: 200px;">
            <marquee behavior="scroll" direction="left" scrollamount="10" 
                     style="font-size: 24px; color: #00CCFF; font-weight: bold; font-family: sans-serif;">
                🚀 Welcome to SQLens: The Future of Automatic SQL Query Generation! 
                Streamline your workflow. Maximize your productivity. 📈
            </marquee>
        </div>
    """
    st.markdown(scrolling_text_html, unsafe_allow_html=True)
st.title("SQLens 🔍")
st.subheader("AI Powered SQL Query Generator")

question = st.text_input("Enter your query request")

if st.button("Generate SQL Query"):

    if question:

        with st.spinner("Generating SQL..."):
            sql_query = get_gemini_res(question, prompt)

        st.code(sql_query, language="sql")

        result = read_sql_query(sql_query, "student.db")

        if isinstance(result, str):
            st.error(result)
        else:
            st.subheader("Query Result")
            st.dataframe(result)


    else:
        st.warning("Please enter a question.")

st.markdown("---")
st.markdown("Built with ❤️ using Gemini + Streamlit")