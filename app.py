import streamlit as st
import sqlite3
import pandas as pd

# ... (نفس إعدادات قاعدة البيانات السابقة)

# إضافة أيقونة البحث في الواجهة
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة", "🔍 البحث القانوني", "📊 سجل المتابعة"])

with tab4:
    st.subheader("🔍 البحث في سجل القضايا")
    search_term = st.text_input("اكتب كلمة للبحث (اسم خصم، رقم قضية، أو موضوع):")
    
    if search_term:
        conn = sqlite3.connect('legal_system.db')
        # بحث في جميع الأعمدة
        query = f"SELECT * FROM cases WHERE المحكمة LIKE '%{search_term}%' OR الموضوع LIKE '%{search_term}%' OR المدعي LIKE '%{search_term}%'"
        df_search = pd.read_sql(query, conn)
        conn.close()
        
        if not df_search.empty:
            st.dataframe(df_search, use_container_width=True)
        else:
            st.warning("لم يتم العثور على نتائج.")
            st.info("💡 نصيحة: تأكد من كتابة اسم القضية أو رقمها بشكل صحيح.")

# ... (باقي الكود)
