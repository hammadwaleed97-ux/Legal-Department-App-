import streamlit as st
import sqlite3
import pandas as pd

# الهيدر المنسق
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 10px; border-radius: 8px; color: white; text-align: center;">
        <h3 style="margin: 0; font-size: 16px;">الإدارة العامة للشئون القانونية - منطقة البحيرة</h3>
    </div>
""", unsafe_allow_html=True)

# استخدام القائمة الجانبية للتنقل (حل مشكلة التداخل)
menu = st.sidebar.selectbox("القائمة الرئيسية", 
    ["⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة", "🔍 البحث القانوني", "📊 سجل المتابعة"])

if menu == "⚖️ قضاء عادي":
    st.subheader("⚖️ قضاء عادي")
    # ضع هنا كود فورم القضاء العادي
elif menu == "🔍 البحث القانوني":
    st.subheader("🔍 البحث القانوني")
    search_term = st.text_input("اكتب كلمة للبحث:")
    # ضع هنا كود البحث
# وهكذا لباقي الأقسام
