import streamlit as st

# 1. إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# 2. كود CSS القسري (لضمان الثبات التام ومنع التداخل)
st.markdown("""
<style>
    /* إخفاء زر الطي الافتراضي */
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #0b1e30 !important;
        width: 300px !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* تثبيت القائمة */
    [data-testid="stSidebar"] {
        width: 300px !important;
    }

    /* ضبط المحتوى الرئيسي ليكون بجانب القائمة */
    .stApp {
        margin-right: 300px !important;
    }

    /* تنسيق النصوص في القائمة */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-family: sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# 3. بناء القائمة الجانبية
with st.sidebar:
    st.markdown("### 🏛️ الهيئة القومية للتأمين")
    st.markdown("---")
    menu = ["🏠 الرئيسية", "📊 لوحة التحكم", "⚖️ الإدارة العامة للقضايا", "💡 الفتوى والتشريع", "📝 التحقيقات", "📚 المكتبة القانونية"]
    choice = st.radio("القائمة الرئيسية", menu, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("مع تحيات وليد حماد")
    st.caption("الادارة العامة للشؤون القانونية")
    st.caption("ديوان عام منطقة البحيرة")

# 4. المحتوى الرئيسي
st.title("لوحة تحكم ديوان عام منطقة البحيرة")
st.write("مرحباً بك في نظام الإدارة القانونية المتطور.")

# بطاقات إحصائية (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("إجمالي القضايا", "15")
col2.metric("القضايا المنتهية", "10")
col3.metric("تحت الإجراء", "5")

# جدول القضايا
st.header("سجل القضايا")
st.table({
    "الرقم": ["2024/101", "2024/102", "2024/103"],
    "الموضوع": ["طلب فتوى", "دعوى قضائية", "تحقيق إداري"],
    "الحالة": ["مؤجلة", "جارية", "مغلقة"]
})
