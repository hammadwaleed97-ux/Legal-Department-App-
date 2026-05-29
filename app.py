import streamlit as st

# إعداد الصفحة لتكون بوضع العرض العريض
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تنسيق CSS لضمان بقاء العناصر ظاهرة دائماً (حتى في الموبايل)
st.markdown("""
    <style>
    .main-menu { background-color: #1a252f; padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px; }
    .menu-item { color: #bdc3c7; margin: 5px 0; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# تقسيم الصفحة إلى قسمين (القائمة على اليمين والمحتوى على اليسار)
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("""
        <div class="main-menu">
            <h3 style="font-size: 16px;">الهيئة القومية للتأمين الاجتماعي</h3>
            <p style="font-size: 12px;">إعداد: وليد حماد - ديوان عام منطقة البحيرة</p>
            <hr>
            <div class="menu-item">🏛️ الإدارة العامة للقضايا</div>
            <div class="menu-item">📁 تسجيل الدعاوى</div>
            <div class="menu-item">📋 تسجيل الطعون</div>
            <div class="menu-item">📝 مذكرة دفاع</div>
            <div class="menu-item" style="color: #ff4b4b;">🔔 تنبيهات الجلسات (قبل أسبوع)</div>
            <div class="menu-item" style="color: #ff4b4b;">🔔 تنبيهات الطعون (قبل 15 يوم)</div>
            <hr>
            <div class="menu-item">💡 الإدارة العامة للفتوى</div>
            <div class="menu-item">📚 المكتبة القانونية</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.title("لوحة تحكم الإدارة القانونية")
    st.info("تم تحويل القائمة لتظهر بجانب المحتوى بدلاً من Sidebar، وبذلك لن تختفي أبداً.")
    st.write("الآن يمكنك البدء في برمجة المهام عند الضغط على كل عنصر.")
