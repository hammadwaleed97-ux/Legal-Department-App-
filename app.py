import streamlit as st
import sqlite3
import pandas as pd

# إعداد الصفحة لتكون واسعة
st.set_page_config(layout="wide")

# الهيدر الموحد
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 10px; border-radius: 8px; color: white; text-align: center;">
        <h4 style="margin: 0;">الإدارة العامة للشئون القانونية - منطقة البحيرة</h4>
    </div>
""", unsafe_allow_html=True)

# القائمة الجانبية الموحدة
menu = st.sidebar.radio("القائمة الرئيسية", 
    ["⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة", "🔍 البحث القانوني", "📊 سجل المتابعة"])

# عرض المحتوى بناءً على الاختيار
if menu == "⚖️ قضاء عادي":
    st.header("⚖️ تسجيل قضاء عادي")
    # هنا تضع فورم الإدخال الخاص بك
elif menu == "🔍 البحث القانوني":
    st.header("🔍 البحث القانوني")
    # هنا تضع كود البحث
# وهكذا...
