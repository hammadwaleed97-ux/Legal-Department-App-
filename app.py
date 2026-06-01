import streamlit as st
import sqlite3
import pandas as pd

# 1. إعداد قواعد البيانات (قضايا + مكتبة)
def init_db():
    conn = sqlite3.connect('legal_system.db')
    c = conn.cursor()
    # جدول القضايا
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY, court TEXT, case_no TEXT, circle TEXT, year TEXT, details TEXT)''')
    # جدول المكتبة
    c.execute('''CREATE TABLE IF NOT EXISTS library 
                 (id INTEGER PRIMARY KEY, category TEXT, title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 2. الهيدر الموحد
def show_header():
    st.markdown("""
        <div style="background-color: #1a3a6e; padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
            <h3>الهيئة القومية للتأمين الاجتماعي</h3>
            <p>الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>
            <p>إعداد: أ/ وليد حماد</p>
        </div>
        """, unsafe_allow_html=True)

show_header()

# 3. التبويبات الرئيسية
tab1, tab2 = st.tabs(["⚖️ القسم القضائي", "📚 المكتبة القانونية"])

# --- إدارة القضايا ---
with tab1:
    sub1, sub2, sub3 = st.tabs(["تسجيل قضية جديدة", "سجل القضايا", "إدارة وتعديل"])
    
    with sub1:
        with st.form("case_form"):
            col1, col2 = st.columns(2)
            court = col1.text_input("المحكمة")
            case_no = col2.text_input("رقم الدعوى")
            circle = col1.text_input("الدائرة")
            year = col2.text_input("سنة")
            details = st.text_area("بيانات الخصوم والموضوع")
            if st.form_submit_button("حفظ القضية"):
                conn = sqlite3.connect('legal_system.db')
                c = conn.cursor()
                c.execute("INSERT INTO cases (court, case_no, circle, year, details) VALUES (?,?,?,?,?)", (court, case_no, circle, year, details))
                conn.commit()
                conn.close()
                st.success("تم حفظ القضية!")

    with sub2:
        conn = sqlite3.connect('legal_system.db')
        df = pd.read_sql("SELECT * FROM cases", conn)
        conn.close()
        st.dataframe(df)

    with sub3:
        case_id = st.number_input("أدخل رقم (ID) القضية للإجراء", min_value=1)
        col_a, col_b = st.columns(2)
        if col_a.button("حذف القضية"):
            conn = sqlite3.connect('legal_system.db')
            c = conn.cursor()
            c.execute("DELETE FROM cases WHERE id=?", (case_id,))
            conn.commit()
            conn.close()
            st.warning("تم الحذف.")

# --- إدارة المكتبة ---
with tab2:
    st.subheader("إدارة المكتبة القانونية")
    cat = st.selectbox("نوع التشريع", ["قوانين", "لوائح", "قرارات وزارية", "كتب دورية"])
    title = st.text_input("عنوان المستند")
    content = st.text_area("نص التشريع أو ملخصه")
    
    if st.button("إضافة للمكتبة"):
        conn = sqlite3.connect('legal_system.db')
        c = conn.cursor()
        c.execute("INSERT INTO library (category, title, content) VALUES (?,?,?)", (cat, title, content))
        conn.commit()
        conn.close()
        st.success("تمت الإضافة!")
        
    st.write("---")
    conn = sqlite3.connect('legal_system.db')
    lib_df = pd.read_sql("SELECT * FROM library", conn)
    conn.close()
    st.dataframe(lib_df)
