import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

=====================================

إعداد الصفحة

=====================================

st.set_page_config(
page_title="إدارة القضايا",
page_icon="⚖️",
layout="wide"
)

=====================================

الاتصال بقاعدة البيانات

=====================================

conn = sqlite3.connect(
"cases.db",
check_same_thread=False
)

cur = conn.cursor()

=====================================

جدول القضايا

=====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

litigation_type TEXT,

claimant_type TEXT,
claimant TEXT,

defendant_type TEXT,
defendant TEXT,

case_no TEXT,
judicial_year TEXT,

circuit TEXT,
case_type TEXT,

court TEXT,
court_name TEXT,

appeal_office TEXT,

subject TEXT,

session_date TEXT,

reason TEXT,

notes TEXT,

judgment_result TEXT,

mobile TEXT,

notifications_enabled INTEGER DEFAULT 1,

status TEXT DEFAULT 'متداولة',

created_at TEXT

)
""")

=====================================

جدول المتابعات

=====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS case_updates(

id INTEGER PRIMARY KEY AUTOINCREMENT,

case_id INTEGER,

update_date TEXT,

adjournment_reason TEXT,

next_session_date TEXT,

status_reason TEXT

)
""")

=====================================

جدول القضايا المحذوفة

=====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS deleted_cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

original_case_id INTEGER,

litigation_type TEXT,

claimant TEXT,

defendant TEXT,

case_no TEXT,

judicial_year TEXT,

subject TEXT,

delete_reason TEXT,

deleted_at TEXT

)
""")

=====================================

جدول سجل التنبيهات

=====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS notifications(

id INTEGER PRIMARY KEY AUTOINCREMENT,

case_id INTEGER,

mobile TEXT,

notification_type TEXT,

sent_at TEXT,

status TEXT

)
""")

conn.commit()

=====================================

ترقيات قواعد البيانات القديمة

=====================================

try:
cur.execute(
"ALTER TABLE cases ADD COLUMN appeal_office TEXT"
)
except:
pass

try:
cur.execute(
"ALTER TABLE cases ADD COLUMN notifications_enabled INTEGER DEFAULT 1"
)
except:
pass

conn.commit()
