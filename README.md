# SQLens:
Secure LLM-powered SQL generation system built with Streamlit, SQLite, and Gemini API. Converts natural language to safe, validated SQL queries with multi-layer protection including SELECT-only enforcement, read-only DB execution, and injection prevention.
🚀 SQLens – Secure AI-Powered SQL Query Generator
🔍 Overview
SQLens is a secure natural language to SQL query generation system built using Streamlit, SQLite, and Google Gemini (v1 API).
It enables administrators to query structured databases using plain English while enforcing strict safety controls to prevent destructive or unsafe database operations.

**🎯 Key Highlights:**
Converts natural language → executable SQL
Enforces SELECT-only query execution
Blocks multi-statement injection attempts
Runs database in read-only mode
Sanitizes LLM output before execution
Dynamically extracts schema metadata for structured display

**🔐 Security Architecture:**
The system implements layered protection:
Application-level SQL validation
Destructive keyword filtering
Multi-statement blocking
Read-only database connection
Prompt-level constraint enforcement

This prevents:
DROP TABLE
DELETE / UPDATE / INSERT
Schema modification
Prompt injection attacks

**🛠 Tech Stack:**
Frontend: Streamlit
Backend: Python
Database: SQLite
LLM: Google Gemini 2.5 Flash
Data Handling: Pandas

**📌 Why This Project Matters:**
This project demonstrates safe integration of Large Language Models into structured data systems. It highlights prompt engineering, defensive programming, API integration, and secure database execution practices.
It simulates real-world AI-driven data access systems used in business intelligence tools.

**🚀 Run Locally:**
git clone https://github.com/your-username/sqlens.git
cd sqlens
pip install -r requirements.txt
streamlit run app.py
**Add your API key in .env:**
GOOGLE_API_KEY=your_api_key_here

