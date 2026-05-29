import streamlit as st

# إعداد الصفحة لتكون بوضع العرض العريض
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تنسيق CSS ليتناسب مع طلبك
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1a252f; color: #aeb9c5; }
    .logo-box { text-align: center; color: white; padding-bottom: 20px; border-bottom: 1px solid #333; }
    .author { color: #3498db; font-weight: bold; margin-top: 10px; font-size: 14px; }
    .stButton>button { width: 100%; border-radius: 5px; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.markdown("""
        <div class="logo-box">
            <h3>الهيئة القومية للتأمين الاجتماعـــــــي</h3>
            <p>الإدارة العامة للشئون القانونية</p>
            <div class="author">إعداد: وليد حماد<br>ديوان عام منطقة البحيرة</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("الإدارة العامة للقضايا")
    if st.button("📁 تسجيل الدعاوى"): pass
    if st.button("📋 تسجيل الطعون"): pass
    if st.button("📝 مذكرة دفاع"): pass
    st.error("🔔 تنبيهات الجلسات (قبل أسبوع)")
    st.error("🔔 تنبيهات الطعون (قبل 15 يوم)")
    
    st.subheader("الإدارة العامة للفتوى")
    if st.button("💡 الفتاوى القانونية"): pass
    if st.button("✏️ إصابات العمل"): pass
    
    st.subheader("المكتبة والأرشيف")
    if st.button("📚 المكتبة القانونية"): pass

# المحتوى الرئيسي
st.title("لوحة تحكم الإدارة القانونية")
st.write("مرحباً بك أستاذ وليد، النظام يعمل الآن عبر Streamlit.")
st.info("النظام جاهز للربط مع أدوات الذكاء الاصطناعي ومعالجة المستندات.")
