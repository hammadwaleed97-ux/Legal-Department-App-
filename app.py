import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import base64

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="نظام الإدارة القانونية - الهيئة القومية للتأمين الاجتماعي",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== SAFE CSS ==================
st.markdown("""
<style>
    .stApp { direction: rtl; text-align: right; }
    div[data-testid="stSidebar"] { direction: rtl; }
</style>
""", unsafe_allow_html=True)

# ================== DATA PERSISTENCE ==================
DATA_FILE = "legal_system_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {
        "cases": [], "appeals": [], "fatwas": [], 
        "investigations": [], "library": [], "archive": [], "activities": []
    }

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================== MAIN UI ==================
st.title("⚖️ الهيئة القومية للتأمين الاجتماعي")
st.subheader("الإدارة العامة للشئون القانونية")
st.markdown("---")

# تجربة عرض بسيطة للتأكد من عمل الكود
st.success("تم تشغيل النظام بنجاح!")
st.write("مرحباً بك في نظام الإدارة القانونية.")

# ================== FOOTER ==================
st.markdown("---")
st.markdown("**مع تحيات وليد حماد الادارة العامة للشءون القانونية ديوان عام منطقة البحيرة**")
