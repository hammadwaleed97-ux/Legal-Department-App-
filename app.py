import streamlit as st

# 1. إعداد الصفحة لتعمل بكامل العرض
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# 2. التنسيق: إطار أزرق داكن يملأ الصفحة + تنسيق الخطوط
st.markdown("""
    <style>
    /* جعل الهامش الجانبي يتناسب مع اللون */
    [data-testid="stSidebar"] { background-color: #0b1e30 !important; color: white; }
    
    /* الإطار الأزرق الكامل في الصفحة الرئيسية */
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 40px;
        border-radius: 20px;
        color: #ffffff;
        text-align: center;
        margin: -10px -10px 20px -10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .main-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 10px; }
    .sub-title { font-size: 1.2rem; color: #a0c4e0; margin-bottom: 5px; }
    .org-name { font-size: 1.5rem; font-weight: bold; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. عرض الهوية داخل الإطار
st.markdown("""
    <div class="header-frame">
        <div style="font-size: 4rem; margin-bottom: 10px;">⚖️</div>
        <div class="org-name">الهيئة القومية للتأمين الاجتماعي</div>
        <div class="main-title">الإدارة العامة للشؤون القانونية</div>
        <div class="sub-title">ديوان عام منطقة البحيرة</div>
    </div>
    """, unsafe_allow_html=True)

# 4. سهم توجيهي بسيط
st.markdown("<div style='text-align:center; font-size:2.5rem; margin-bottom:20px;'>⬇️</div>", unsafe_allow_html=True)

# 5. القائمة الجانبية (للتنقل)
st.sidebar.title("🏛️ القائمة الرئيسية")
choice = st.sidebar.radio("اختر القسم", ["الرئيسية", "القضايا", "الفتاوى", "التحقيقات"])

# 6. ربط المحتوى بالصفحة
if choice == "الرئيسية":
    st.success("مرحباً بك في نظام الإدارة الذكي - ديوان عام منطقة البحيرة")
    st.write("استخدم القائمة الجانبية للانتقال بين الأقسام.")

st.sidebar.markdown("---")
st.sidebar.write("مع تحيات وليد حماد")
