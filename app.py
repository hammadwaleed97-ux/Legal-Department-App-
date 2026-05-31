import streamlit as st
import sqlite3
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# 2. التنسيق باللون الأزرق الداكن (هوية الإدارة)
st.markdown("""
    <style>
    /* اللون الأساسي للأزرق الداكن */
    [data-testid="stSidebar"] { background-color: #0b1e30 !important; }
    
    /* تنسيق العناوين والأيقونات */
    .title-box { 
        background: linear-gradient(135deg, #0b1e30, #2c5f9e); 
        padding: 25px; 
        border-radius: 15px; 
        color: white; 
        text-align: center; 
        margin-bottom: 20px;
    }
    .icon-style { font-size: 3rem; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. محتوى الصفحة الرئيسية
if "menu" not in st.session_state: st.session_state.menu = "الرئيسية"

# العنوان مع الأيقونات
st.markdown("""
    <div class="title-box">
        <div class="icon-style">⚖️</div>
        <h1>ديوان عام منطقة البحيرة</h1>
        <p>الإدارة العامة للشؤون القانونية — نظام التحكم الذكي</p>
    </div>
    """, unsafe_allow_html=True)

# إضافة سهم توجيهي (كعنصر جذب)
st.markdown("<div style='text-align:center; font-size:2rem;'>⬇️</div>", unsafe_allow_html=True)

# عرض الأيقونات التوضيحية
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("📁 إحصاء القضايا")
with col2:
    st.info("📝 الفتاوى")
with col3:
    st.info("🔍 التحقيقات")
with col4:
    st.info("📚 المكتبة")

# قائمة التنقل (التي ستظهر في الموبايل بالضغط على السهم)
st.sidebar.title("🏛️ القائمة الرئيسية")
choice = st.sidebar.radio("اختر القسم", ["الرئيسية", "القضايا", "الفتاوى", "التحقيقات"])

st.sidebar.markdown("---")
st.sidebar.write("مع تحيات وليد حماد")
