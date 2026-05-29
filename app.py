import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تنسيق CSS لجعل القائمة والأيقونات ظاهرة وتنسيق اللوجو
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1a252f; color: #ffffff; padding: 20px; }
    .logo-box { text-align: center; color: white; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 15px; }
    .author-info { font-size: 14px; color: #3498db; margin-top: 10px; line-height: 1.6; }
    .menu-btn { font-size: 16px; margin: 10px 0; color: #ffffff; }
    .alert-box { color: #ff4b4b; font-weight: bold; background: #2c3e50; padding: 10px; border-radius: 5px; margin: 5px 0; }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي (القائمة)
with st.sidebar:
    st.markdown("""
        <div class="logo-box">
            <h3>الهيئة القومية للتأمين الاجتماعـــــــي</h3>
            <p>الإدارة العامة للشئون القانونية</p>
            <div class="author-info">
                إعداد: وليد حماد<br>
                ديوان عام منطقة البحيرة
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏛️ الإدارة العامة للقضايا")
    st.markdown("📁 تسجيل الدعاوى")
    st.markdown("📋 تسجيل الطعون")
    st.markdown("📝 مذكرة دفاع")
    st.markdown('<div class="alert-box">🔔 تنبيهات الجلسات (قبل أسبوع)</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-box">🔔 تنبيهات الطعون (قبل 15 يوم)</div>', unsafe_allow_html=True)
    
    st.markdown("### 💡 الإدارة العامة للفتوى")
    st.markdown("💡 الفتاوى القانونية")
    st.markdown("✏️ إصابات العمل")
    
    st.markdown("### 📚 المكتبة والأرشيف")
    st.markdown("📚 المكتبة القانونية")

# المحتوى الرئيسي
st.title("لوحة تحكم الإدارة القانونية")
st.success("مرحباً بك أستاذ وليد، تم تحديث الواجهة لتكون الأيقونات ظاهرة دائماً.")
st.write("النظام الآن مجهز بالكامل للمرحلة القادمة: ربط ملفات المكتبة والتحقيقات بالذكاء الاصطناعي.")
