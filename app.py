import streamlit as st

st.set_page_config(page_title="الشؤون القانونية - البحيرة", layout="wide", initial_sidebar_state="collapsed")

# CSS
st.markdown("""
<style>
* { font-family: 'Cairo', Tahoma, sans-serif; direction: rtl; }
.header { text-align:center; border-bottom:3px solid #0d47a1; padding-bottom:15px; margin-bottom:25px; }
.header h1 { color:#0d47a1; font-size:22px; }
.header h2 { color:#1565c0; font-size:18px; }
.btn { background:#1976d2; color:#fff; border:none; padding:10px 18px; border-radius:6px; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
  <h1>الهيئة القومية للتأمين الاجتماعي - الإدارة العامة للشؤون القانونية</h1>
  <h2>ديوان عام منطقة: البحيرة</h2>
</div>
""", unsafe_allow_html=True)

# Tabs بدل Nav
tab1, tab2, tab3, tab4 = st.tabs(["التقارير", "الأرشيف", "القضايا المحذوفة", "البحث عن دعوى"])

with tab1:
    st.subheader("التقارير")
    bayan = st.selectbox("بيان", ["بالقضايا", "بالأحكام"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: manteqa = st.text_input("اسم المنطقة", "البحيرة")
    with col2: ostaz = st.text_input("اسم الأستاذ", "وليد شعبان حماد")
    with col3: from_date = st.date_input("من تاريخ")
    with col4: to_date = st.date_input("إلى تاريخ")
    
    if st.button("عرض التقرير", type="primary"):
        if bayan == "بالقضايا":
            st.info(f"كشف بالدعاوى المتداولة من {from_date} حتى {to_date} طرف الأستاذ / {ostaz}")
            st.dataframe([{
                "م": 1, "رقم الدعوى": 123, "السنة": 2025, "المحكمة": "دمنهور",
                "الخصوم": "أحمد ضد الهيئة", "الموضوع": "مطالبة", "آخر إجراء": "جلسة 12/5/2026"
            }])
        else:
            ahkam_type = st.selectbox("نوع الأحكام", ["للصالح والضد", "للصالح", "للضد"])
            st.info(f"بيان بالأحكام {ahkam_type} من {from_date} حتى {to_date}")
            st.dataframe([{
                "م": 1, "رقم الدعوى": 456, "تاريخ الحكم": "10/3/2026",
                "المنطوق": "قبول الدعوى", "الصالح/الضد": "الصالح"
            }])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.button("فتح التقرير")
    col2.button("تحميل PDF")
    col3.button("تحميل Word")
    col4.button("طباعة")

with tab2:
    st.subheader("أرشيف الأحكام المحكوم فيها")
    st.dataframe([{
        "م": 1, "رقم الدعوى": 456, "السنة": 2024, "المحكمة": "ابتدائية",
        "الخصوم": "محمد ضد الهيئة", "تاريخ الحكم": "10/3/2026", "النتيجة": "الصالح"
    }])
    if st.button("إضافة الإجراء المتخذ"):
        ejra = st.radio("اختر الإجراء", ["تم الطعن", "حفظ"])
        if ejra == "تم الطعن":
            st.text_input("رقم الطعن")
            st.text_area("بيانات الطعن")
            st.button("حفظ للأرشيف")

with tab3:
    st.subheader("القضايا المحذوفة")
    st.dataframe([{
        "م": 1, "رقم الدعوى": 999, "السنة": 2023, "الخصوم": "سعيد ضد الهيئة",
        "تاريخ الحذف": "1/1/2026", "سبب الحذف": "تصالح"
    }])
    if st.button("فتح القضية"):
        st.success("بيانات القضية المحذوفة كاملة حتى تاريخ الحذف وسببه")

with tab4:
    st.subheader("البحث عن دعوى")
    col1, col2, col3 = st.columns(3)
    with col1: name = st.text_input("الاسم")
    with col2: num = st.text_input("رقم الدعوى/الاستئناف/الطعن")
    with col3: year = st.number_input("السنة", min_value=2000, max_value=2030)
    
    if st.button("بحث"):
        st.dataframe([{
            "رقم الدعوى": num or 123, "السنة": year or 2025,
            "الخصوم": f"{name or 'أحمد'} ضد الهيئة", "الموضوع": "مطالبة"
        }])
        st.button("فتح الدعوى/الاستئناف/الطعن بكل بياناتها")
