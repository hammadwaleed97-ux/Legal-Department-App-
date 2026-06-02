import streamlit as st
import sqlite3
import pandas as pd

# 1. تهيئة قاعدة البيانات (تخزين دائم للقضايا)
def init_db():
    conn = sqlite3.connect('legal_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, نوع_القضية TEXT, المحكمة TEXT, رقم_الدعوى TEXT, 
                  السنة TEXT, المدعي TEXT, المدعى_عليه TEXT, الموضوع TEXT, تاريخ_الجلسة DATE, الحالة TEXT)''')
    conn.commit()
    conn.close()
init_db()

# 2. الهيدر المنسق (سطر واحد)
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 15px; border-radius: 8px; color: white; text-align: center; margin-bottom: 20px;">
        <h3 style="margin: 0; font-size: 18px;">الهيئة القومية للتأمين الاجتماعي - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</h3>
        <p style="margin: 0; font-size: 12px;">إعداد: أ/ وليد حماد</p>
    </div>
""", unsafe_allow_html=True)

# 3. الرابط الجذري للمكتبة (تم ربطه بنجاح)
DRIVE_LINK = "https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke" 
st.markdown(f'''
    <div style="text-align: center; margin-bottom: 20px;">
        <a href="{DRIVE_LINK}" target="_blank" 
        style="background-color: #28a745; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">
        📂 مكتبة الإدارة القانونية (Google Drive)
        </a>
    </div>
''', unsafe_allow_html=True)

# 4. الأقسام القضائية (الأيقونات والتصنيفات)
tab1, tab2, tab3, tab4 = st.tabs(["⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة", "📊 سجل المتابعة والتقارير"])

def save_case_to_db(c_type, court, no, year, p, d, details, date, status):
    conn = sqlite3.connect('legal_system.db')
    c = conn.cursor()
    c.execute("INSERT INTO cases VALUES (NULL,?,?,?,?,?,?,?,?,?)", 
              (c_type, court, no, year, p, d, details, date, status))
    conn.commit()
    conn.close()

def render_form(c_type):
    with st.form(f"form_{c_type}"):
        c1, c2 = st.columns(2)
        court = c1.text_input("المحكمة")
        case_no = c2.text_input("رقم الدعوى")
        year = c1.text_input("السنة")
        plaintiff = c2.text_input("اسم المدعي")
        defendant = st.text_input("اسم المدعى عليه")
        date = st.date_input("تاريخ الجلسة")
        details = st.text_area("الموضوع / الوقائع")
        status = st.selectbox("حالة القضية", ["متداولة", "محجوزة للحكم", "صدر حكم"])
        
        if st.form_submit_button("حفظ القضية في السجل"):
            save_case_to_db(c_type, court, case_no, year, plaintiff, defendant, details, date, status)
            st.success("تم الحفظ!")

with tab1: render_form("قضاء عادي")
with tab2: render_form("محكمة النقض")
with tab3: render_form("مجلس الدولة")

with tab4:
    st.subheader("سجل المتابعة")
    conn = sqlite3.connect('legal_system.db')
    df = pd.read_sql("SELECT * FROM cases", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
