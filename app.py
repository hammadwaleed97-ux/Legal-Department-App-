import streamlit as st

# الإعدادات
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق
st.markdown("""
    <style>
    [data-testid='stSidebar'], header { display: none !important; }
    .header-frame { background: linear-gradient(135deg, #0b1e30, #1a3a6e); padding: 20px; color: white; text-align: center; border-radius: 0 0 20px 20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""<div class="header-frame"><h3>الهيئة القومية للتأمين الاجتماعـــــــي</h3><p>الإدارة العامة للشئون القانونية | مع تحيات أ/ وليد حماد</p></div>""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

if st.session_state.page == "الرئيسية":
    show_header()
    st.write("### لوحة التحكم الرئيسية")
    # تم تعديل اسم الزر هنا
    if st.button("📁 إدارة القضايا"): st.session_state.page = "القضايا"; st.rerun()
    if st.button("📝 الفتاوى"): st.session_state.page = "الفتاوى"; st.rerun()
    if st.button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"; st.rerun()
    if st.button("📚 المكتبة"): st.session_state.page = "المكتبة"; st.rerun()
    if st.button("📦 الأرشيف"): st.session_state.page = "الأرشيف"; st.rerun()

elif st.session_state.page == "القضايا":
    show_header()
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()
    
    st.header("📁 إدارة القضايا")
    
    # الترتيب الذي طلبته تماماً
    # 1. المحتوى القضائي (الذي أرسلت تفاصيله الكثيرة)
    # 2. التنبيهات
    # 3. التقارير
    
    section1, section2, section3 = st.tabs(["القسم القضائي", "🔔 التنبيهات", "📊 التقارير"])
    
    with section1:
        st.subheader("أولاً: الإدارة العامة للقضايا - القسم القضائي")
        # هنا سنضع التفاصيل الكثيرة التي أرسلتها (المحاكم الابتدائية، الاستئنافية، النقض، مجلس الدولة)
        st.info("جاري إدراج هيكل المحاكم والقضايا بناءً على المعطيات...")
        
    with section2:
        st.subheader("ثانياً: التنبيهات")
        st.write("نظام متابعة التنبيهات الخاص بالقضايا.")
        
    with section3:
        st.subheader("ثالثاً: التقارير")
        st.write("نظام تقارير الإنجاز.")
