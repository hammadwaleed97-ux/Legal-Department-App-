import streamlit as st
import pandas as pd

# [إعدادات الهوية - ثابتة]
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")
st.markdown("""
    <style>
    .header-frame { background: linear-gradient(135deg, #0b1e30, #1a3a6e); padding: 25px; color: #ffffff; text-align: center; border-radius: 0 0 20px 20px; }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""
        <div class="header-frame">
            <h3>الهيئة القومية للتأمين الاجتماعـــــــي</h3>
            <p>الإدارة العامة للشئون القانونية | مع تحيات أ/ وليد حماد</p>
        </div>
        """, unsafe_allow_html=True)

show_header()

# [نظام إدارة قسم القضايا]
st.subheader("أولاً: الإدارة العامة للقضايا - القسم القضائي")

# القائمة الفرعية للقضاء العادي
c_type = st.radio("اختر نوع المحاكم:", ["المحاكم الابتدائية", "المحاكم الاستئنافية", "محكمة النقض"], horizontal=True)

if c_type == "المحاكم الابتدائية":
    sub_task = st.selectbox("اختر الإجراء:", ["صياغة مذكرة بدفاع (الهيئة مدعى عليها)", "صياغة مذكرة بدفاع (الهيئة مدعية)"])
    
    with st.expander("بيانات الدعوى والمستندات"):
        col1, col2 = st.columns(2)
        court = col1.text_input("المحكمة")
        circuit = col2.text_input("الدائرة")
        case_num = col1.text_input("رقم الدعوى")
        case_year = col2.text_input("لسنة")
        p1 = st.text_input("اسم المدعى وصفته")
        p2 = st.text_input("اسم المدعى عليه وصفته")
        facts = st.text_area("ملخص الوقائع أو ارفع صورة الصحيفة")
        file_upload = st.file_uploader("رفع صورة الصحيفة لقراءتها", type=['pdf', 'jpg', 'png'])

    if st.button("صياغة المذكرة"):
        st.info("جاري استخدام الذكاء الاصطناعي لصياغة المذكرة وترتيب الدفوع قانونياً...")
        # هنا سيتم ربط الـ API الخاص بـ Gemini لقراءة الملفات والصياغة
        st.success("تمت الصياغة بنجاح")
        st.write("--- نص المذكرة المقترح ---")
        st.write("مذكرة بدفاع الهيئة القومية للتأمين الاجتماعي (بصفتها...)")
        # التوقيعات المطلوبة
        st.markdown("<br><br><b>عن الهيئة:</b><br>____________________<br><b>عضو الإدارة القانونية</b> ⠀⠀⠀⠀⠀⠀ <b>مدير الإدارة القانونية</b>", unsafe_allow_html=True)

    st.download_button("حفظ بصيغة Word", "محتوى المذكرة", file_name="مذكرة_دفاع.docx")
    st.download_button("حفظ بصيغة PDF", "محتوى المذكرة", file_name="مذكرة_دفاع.pdf")

# (سيتم إضافة باقي الأقسام الاستئنافية والنقض بنفس هذا المنطق)
