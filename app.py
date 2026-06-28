import streamlit as st
import sqlite3
from datetime import datetime
import os

# =====================================
# إعداد الصفحة
# =====================================

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# Session State
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

# =====================================
# قاعدة البيانات
# =====================================

conn = sqlite3.connect(
    "cases.db",
    check_same_thread=False
)

cur = conn.cursor()

# =====================================
# جدول القضايا
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

case_type TEXT,
court_type TEXT,
court_name TEXT,
mission TEXT,

case_number TEXT,
judicial_year TEXT,
circuit TEXT,
case_category TEXT,

plaintiff TEXT,
defendant TEXT,

subject TEXT,

notes TEXT,

whatsapp_enabled INTEGER,
whatsapp_number TEXT,

created_at TEXT

)
""")

# =====================================
# جدول الجلسات
# =====================================

cur.execute("""

CREATE TABLE IF NOT EXISTS sessions(

id INTEGER PRIMARY KEY AUTOINCREMENT,

case_id INTEGER,

session_date TEXT,

roll_number TEXT,

procedure TEXT,

created_at TEXT

)

""")

# =====================================
# جدول المستندات
# =====================================

cur.execute("""

CREATE TABLE IF NOT EXISTS documents(

id INTEGER PRIMARY KEY AUTOINCREMENT,

case_id INTEGER,

document_type TEXT,

document_description TEXT,

file_name TEXT,

file_path TEXT,

uploaded_at TEXT

)

""")

conn.commit()
