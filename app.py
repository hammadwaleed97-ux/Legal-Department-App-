import streamlit as st
import sqlite3
import pandas as pd

# 1. تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('legal_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY, نوع_القضية TEXT, المحكمة TEXT, رقم_الدعوى TEXT, 
                  السنة TEXT, الخصوم TEXT, تاريخ_الجلسة DATE, الحالة TEXT)''')
    conn.commit()
    conn.close()
init_db()

# 2. الهيدر (سطر واحد)
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 10px; border-radius: 8px; color: white; text-align: center;">
        <h3 style="margin: 0; font-size: 18px;">الهيئة القومية للتأمين الاجتماعي - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</h3>
        <p style="margin: 0; font-size: 12px;">إعداد: أ/ وليد حماد</p>
    </div>
""", unsafe_allow_html=True)

# 3. الربط الدائم بالمكتبة (Google Drive)
drive_link = "https://your-drive-folder-link" # ضع رابطك هنا
st.markdown(f'<div style="text-align: center; margin: 15px;"><a href="{drive_link}" target="_blank" style="color: #1a3a6e; font-weight: bold; font-size: 16px;">📂 مكتبة الإدارة (ربط مباشر بـ Google Drive)</a></div>', unsafe_allow_html=True)

# 4. الأقسام القضائية (مع الأيقونات)
tab1, tab2, tab3 = st.tabs(["⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة"])

def render_case_tab(tab_name):
    with st.form(f"form_{tab_name}"):
        col1, col2 = st.columns(2)
        court = col1.text_input("المحكمة")
        case_no = col2.text_input("رقم الدعوى")
        year = col1.text_input("السنة")
        status = col2.selectbox("حالة القضية", ["متداولة", "محجوزة للحكم", "صدر حكم"])
        details = st.text_area("بيانات الخصوم")
        if st.form_submit_button("حفظ القضية"):
            conn = sqlite3.connect('legal_system.db')
            c = conn.cursor()
            c.execute("INSERT INTO cases VALUES (NULL,?,?,?,?,?,?,?)", (tab_name, court, case_no, year, details, "2026-01-01", status))
            conn.commit()
            conn.close()
            st.success("تم الحفظ")

with tab1: render_case_tab("قضاء عادي")
with tab2: render_case_tab("محكمة النقض")
with tab3: render_case_tab("مجلس الدولة")

# 5. عرض سجل القضايا والتقارير
st.divider()
st.subheader("سجل المتابعة والتقارير")
conn = sqlite3.connect('legal_system.db')
df = pd.read_sql("SELECT * FROM cases", conn)
conn.close()
st.dataframe(df, use_container_width=True)
