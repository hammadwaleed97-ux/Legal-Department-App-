import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="إدارة القضايا", layout="centered", initial_sidebar_state="collapsed")

# ===== CSS التصميم القديم بالأزرار الزرقا والخلفية الزرقا الغامق =====
st.markdown("""
<style>
* { font-family: 'Cairo', Tahoma, sans-serif; direction: rtl; }
.stApp { background: #0a1628; }
.header { text-align: center; color: white; font-size: 24px; font-weight: bold; margin: 20px 0; }
.sub-header { text-align: center; color: #cbd5e1; font-size: 16px; margin-bottom: 15px; }
.login-box { background: rgba(255,255,255,0.08); padding: 30px; border-radius: 15px; max-width: 400px; margin: 50px auto; border: 1px solid rgba(255,255,255,0.2); }
.stButton > button {
    width: 100%;
    height: 65px;
    background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.stButton > button:hover { 
    background: linear-gradient(135deg, #1e3a8a 0%, #1e293b 100%);
    transform: translateY(-2px);
}
.case-card {
    background: white;
    color: #0f1b3a;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    margin: 6px;
    min-height: 85px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.name-yellow { color: #fbbf24; font-size: 24px; font-weight: bold; text-align: center; margin: 10px 0; }
.scale-icon { font-size: 65px; text-align: center; margin: 25px 0; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stNumberInput > div > div > input {
    background: rgba(255,255,255,0.95);
    color: #0f1b3a;
    border-radius: 8px;
}
.stSelectbox > div > div > select { background: rgba(255,255,255,0.95); color: #0f1b3a; }
.stDateInput > div > div > input { background: rgba(255,255,255,0.95); color: #0f1b3a; }
</style>
""", unsafe_allow_html=True)

# ===== Session State =====
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'selected_case' not in st.session_state: st.session_state.selected_case = None

# ===== دوال مساعدة =====
def login():
    if st.session_state.username == "waleedhammad" and st.session_state.password == "1234":
        st.session_state.logged_in = True
        st.rerun()
    else: 
        st.error("❌ اسم المستخدم أو كلمة المرور خطأ")

def logout():
    st.session_state.logged_in = False
    st.session_state.page = 'main'
    st.rerun()

# ===== صفحة تسجيل الدخول =====
if not st.session_state.logged_in:
    st.markdown('<div class="scale-icon">⚖️</div>', unsafe_allow_html=True)
    st.markdown('<div class="header">إدارة القضايا</div>', unsafe_allow_html=True)
    st.markdown('<div class="header" style="font-size:20px;">تسجيل الدخول</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.text_input("اسم المستخدم", key="username", value="waleedhammad", placeholder="waleedhammad")
        st.text_input("كلمة المرور", type="password", key="password", placeholder="1234")
        st.button("دخول", on_click=login, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

# ===== بعد تسجيل الدخول =====
else:
    # الهيدر + الاسم بالأصفر
    st.markdown('<div class="scale-icon">⚖️</div>', unsafe_allow_html=True)
    st.markdown('<div class="header">الهيئة القومية للتأمين الاجتماعي</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">الإدارة العامة للشؤون القانونية</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">ديوان عام منطقة: البحيرة</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; color:#cbd5e1; font-size:14px;">مع تحيات</div>', unsafe_allow_html=True)
    st.markdown('<div class="name-yellow">وليد شعبان حماد</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # ===== القائمة الرئيسية - الأزرار الزرقا الكبيرة =====
    if st.session_state.page == 'main':
        st.button("⚖️ تسجيل القضايا", on_click=lambda: st.session_state.update({'page': 'tasksjeel'}))
        st.button("🔔 التنبيهات", on_click=lambda: st.session_state.update({'page': 'tanbihat'}))
        st.button("📊 التقارير", on_click=lambda: st.session_state.update({'page': 'reports'}))
        st.button("📁 أرشيف القضايا", on_click=lambda: st.session_state.update({'page': 'archive'}))
        st.button("📋 حصر عام القضايا", on_click=lambda: st.session_state.update({'page': 'hasr'}))
        st.button("🔍 البحث", on_click=lambda: st.session_state.update({'page': 'search'}))
        st.button("❌ القضايا المحذوفة", on_click=lambda: st.session_state.update({'page': 'deleted'}))
        st.button("🚪 خروج", on_click=logout)
    
    # ===== صفحة ملف القضية - الكروت البيضا 3 في الصف + الجلسات =====
    elif st.session_state.page == 'tasksjeel':
        st.button("⬅️ رجوع للقائمة الرئيسية", on_click=lambda: st.session_state.update({'page': 'main'}))
        st.markdown('<div class="scale-icon" style="font-size:45px;">⚖️ ملف القضية</div>', unsafe_allow_html=True)
        
        # الكروت البيضا 3 في الصف
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown('<div class="case-card">رقم القضية<br><span style="font-size:22px;">7777</span></div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="case-card">السنة القضائية<br><span style="font-size:22px;">140</span></div>', unsafe_allow_html=True)
        with col3: st.markdown('<div class="case-card">الدائرة<br><span style="font-size:18px;">الخامسة عشر</span></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown('<div class="case-card">نوع الدعوى<br><span style="font-size:20px;">مدني</span></div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="case-card">المحكمة<br><span style="font-size:20px;">استئناف</span></div>', unsafe_allow_html=True)
        with col3: st.markdown('<div class="case-card">اسم المحكمة<br><span style="font-size:20px;">القاهرة</span></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1: st.markdown('<div class="case-card">المستأنف<br><span style="font-size:16px;">سعدية مبروك احمد</span></div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="case-card">المستأنف ضده<br><span style="font-size:20px;">الهيئة</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="case-card">موضوع الدعوى / الاستئناف<br><span style="font-size:20px;">عجز</span></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📅 الجلسات")
        df = pd.DataFrame([
            {"الروول": "-", "تاريخ الجلسة": "2026-12-31", "الإجراءات": "للسابق", "الملاحظات": "-"},
            {"الروول": "-", "تاريخ الجلسة": "2026-12-22", "الإجراءات": "للاعطال", "الملاحظات": "-"},
            {"الروول": "-", "تاريخ الجلسة": "2026-09-29", "الإجراءات": "للاعلان", "الملاحظات": "-"}
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("### ➕ إضافة جلسة جديدة")
        col1, col2 = st.columns(2)
        with col1: st.text_input("الروول", key="new_roll")
        with col2: st.date_input("تاريخ الجلسة", key="new_date")
        col1, col2 = st.columns(2)
        with col1: st.text_input("الإجراءات", key="new_action")
        with col2: st.text_area("الملاحظات", key="new_notes", height=80)
        if st.button("إضافة الجلسة", type="primary"):
            st.success("✅ تم إضافة الجلسة بنجاح")
    
    # ===== التقارير - بيان بالقضايا / بيان بالأحكام + للصالح والضد =====
    elif st.session_state.page == 'reports':
        st.button("⬅️ رجوع للقائمة الرئيسية", on_click=lambda: st.session_state.update({'page': 'main'}))
        st.subheader("📊 التقارير")
        
        bayan = st.selectbox("نوع البيان", ["بالقضايا", "بالأحكام"], key="bayan_type")
        col1, col2 = st.columns(2)
        with col1: from_date = st.date_input("من تاريخ", value=date(2026, 1, 1))
        with col2: to_date = st.date_input("إلى تاريخ", value=date(2026, 12, 31))
        ostaz = st.text_input("اسم الأستاذ", "وليد شعبان حماد")
        manteqa = st.text_input("اسم المنطقة", "البحيرة")
        
        if bayan == "بالأحكام":
            ahkam_type = st.selectbox("فلترة الأحكام", ["للصالح والضد", "للصالح", "للضد"])
        
        if st.button("عرض التقرير", type="primary"):
            if bayan == "بالقضايا":
                st.markdown(f"**كشف بالدعاوى المتداولة خلال الفترة من {from_date} حتى {to_date} طرف الأستاذ / {ostaz}**")
                data = [{
                    "م": 1, "رقم الدعوى": 123, "اباستيناف": "-", "ابطعن": "-", "حسب الحالة": "متداولة",
                    "السنة القضائية": 2025, "الدائرة": 3, "النوع": "مدني", "المحكمة": "ابتدائية",
                    "اسم المحكمة": "دمنهور", "المأمورية": "مسجلة", "أسماء الخصوم": "أحمد ضد الهيئة",
                    "موضوع الدعوى": "مطالبة", "الاستئناف": "-", "الطعن": "-", "آخر إجراء": "جلسة 12/5/2026 للاطلاع"
                }]
                st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
            else:
                st.markdown(f"**بيان بالأحكام {ahkam_type} خلال الفترة من {from_date} حتى {to_date} طرف الأستاذ / {ostaz}**")
                data = [{
                    "م": 1, "رقم الدعوى": 456, "اباستيناف": "-", "ابطعن": "-", "حسب الحالة": "محكوم",
                    "السنة القضائية": 2024, "الدائرة": 2, "النوع": "عمال", "المحكمة": "ابتدائية",
                    "اسم المحكمة": "كفر الدوار", "المأمورية": "مسجلة", "أسماء الخصوم": "محمد ضد الهيئة",
                    "موضوع الدعوى": "تعويض", "الاستئناف": "-", "الطعن": "-",
                    "تاريخ الحكم": "10/3/2026", "منطوق الحكم": "قبول الدعوى", "الصالح/الضد": ahkam_type
                }]
                st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.button("فتح التقرير")
        col2.button("تحميل PDF")
        col3.button("تحميل Word")
        col4.button("طباعة التقرير")
        
        st.markdown("---")
        st.subheader("📄 استخراج صور أحكام")
        col1, col2, col3 = st.columns([2,2,1])
        with col1: 
            ahkam_type2 = st.selectbox("النوع", ["للصالح والضد", "للصالح", "للضد"], key="ahkam_filter")
        with col2: 
            ahkam_from = st.date_input("من تاريخ", key="ahkam_from")
        with col3: 
            ahkam_to = st.date_input("حتى تاريخ", key="ahkam_to")
        
        if st.button("استخراج", type="primary"):
            st.dataframe(pd.DataFrame([{
                "رقم الدعوى": 789, "بيانات الحصر الخارجي": "أحمد ضد الهيئة - مدني ابتدائية",
                "تاريخ الحكم": "15/4/2026", "المنطوق": "رفض الدعوى"
            }]), use_container_width=True, hide_index=True)
            st.button("تحميل كل الأحكام Word")
    
    # ===== الأرشيف - إضافة الإجراء المتخذ مع شرط الطعن =====
    elif st.session_state.page == 'archive':
        st.button("⬅️ رجوع للقائمة الرئيسية", on_click=lambda: st.session_state.update({'page': 'main'}))
        st.subheader("📁 أرشيف الأحكام المحكوم فيها")
        st.dataframe(pd.DataFrame([{
            "م": 1, "رقم الدعوى": 456, "السنة": 2024, "المحكمة": "ابتدائية",
            "الخصوم": "محمد ضد الهيئة", "موضوع الدعوى": "تعويض",
            "تاريخ الحكم": "10/3/2026", "المنطوق": "قبول", "النتيجة": "الصالح"
        }]), use_container_width=True, hide_index=True)
        
        if st.button("➕ إضافة الإجراء المتخذ", type="primary"):
            ejra = st.radio("اختر الإجراء", ["تم الطعن", "حفظ"], horizontal=True)
            if ejra == "تم الطعن":
                taan_num = st.text_input("رقم الطعن")
                taan_data = st.text_area("بيانات الطعن")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("حفظ للأرشيف"):
                        st.success("✅ تم حفظ الطعن في الأرشيف - رقم الطعن لا يظهر في تقارير الأحكام")
                with col2:
                    if st.button("إضافة للقضايا المتداولة"):
                        st.success(f"✅ تم إضافة الطعن برقم {taan_num} للقضايا المتداولة")
            else:
                hifz_data = st.text_area("بيانات مذكرة أسباب الحفظ")
                if st.button("حفظ"):
                    st.success("✅ تم حفظ بيانات المذكرة - لا تظهر في تقارير الأحكام")
    
    # ===== القضايا المحذوفة - تفتحها وتشوف كل البيانات وسبب الحذف =====
    elif st.session_state.page == 'deleted':
        st.button("⬅️ رجوع للقائمة الرئيسية", on_click=lambda: st.session_state.update({'page': 'main'}))
        st.subheader("❌ القضايا المحذوفة")
        st.dataframe(pd.DataFrame([{
            "م": 1, "رقم الدعوى": 999, "السنة": 2023, "المحكمة": "ابتدائية",
            "الخصوم": "سعيد ضد الهيئة", "موضوع الدعوى": "مطالبة",
            "تاريخ الحذف": "1/1/2026", "سبب الحذف": "تصالح"
        }]), use_container_width=True, hide_index=True)
        
        if st.button("📂 فتح القضية المحذوفة", type="primary"):
            st.success("📋 بيانات القضية كاملة حتى تاريخ الحذف")
            st.info("**رقم الدعوى:** 999 لسنة 2023")
            st.info("**الخصوم:** سعيد ضد الهيئة")
            st.info("**الموضوع:** مطالبة")
            st.info("**المحكمة:** دمنهور الابتدائية - الدائرة 2")
            st.warning("**تاريخ الحذف:** 1/1/2026 - **سبب الحذف:** تصالح بين الطرفين")
            st.write("**جميع البيانات حتى تاريخ الحذف:** الجلسات، الإجراءات، الملاحظات...")
    
    # ===== البحث - يطلع النتيجة بزر فتح القضية وكل بياناتها =====
    elif st.session_state.page == 'search':
        st.button("⬅️ رجوع للقائمة الرئيسية", on_click=lambda: st.session_state.update({'page': 'main'}))
        st.subheader("🔍 البحث عن دعوى")
        col1, col2, col3 = st.columns(3)
        with col1: name = st.text_input("الاسم")
        with col2: num = st.text_input("رقم الدعوى/الاستئناف/الطعن")
        with col3: year = st.number_input("السنة", min_value=2000, max_value=2030, value=2025)
        
        if st.button("بحث", type="primary"):
            st.button("📁 فتح القضية")
            st.markdown("**سعدية مبروك احمد ضد الهيئة - عجز - جلسة 13-06-2026 - أول جلسة**")
            st.caption("الخامسة عشر مدني القاهرة - 7777/140")
            st.button("📁 فتح القضية")
            st.markdown("**سلامة سعد محمد ضد الهيئة - شيخوخة - جلسة 30-06-2026 - أول جلسة**")
            st.caption("الخامسة عشر مدني القاهرة - 8888/141")
    
    # ===== باقي الصفحات =====
    elif st.session_state.page == 'tanbihat':
        st.button("⬅️ رجوع للقائمة الرئيسية", on_click=lambda: st.session_state.update({'page': 'main'}))
        st.subheader("🔔 التنبيهات")
        st.info("جلسة سعدية مبروك احمد بتاريخ 13-06-2026")
        st.info("جلسة سلامة سعد محمد بتاريخ 30-06-2026")
    
    elif st.session_state.page == 'hasr':
        st.button("⬅️ رجوع للقائمة الرئيسية", on_click=lambda: st.session_state.update({'page': 'main'}))
        st.subheader("📋 حصر عام القضايا")
        st.dataframe(pd.DataFrame([
            {"م": 1, "رقم القضية": 7777, "السنة": 140, "الخصوم": "سعدية مبروك ضد الهيئة", "الحالة": "متداولة"},
            {"م": 2, "رقم القضية": 8888, "السنة": 141, "الخصوم": "سلامة سعد ضد الهيئة", "الحالة": "متداولة"}
        ]), use_container_width=True, hide_index=True)
    
    else:
        st.button("⬅️ رجوع للقائمة الرئيسية", on_click=lambda: st.session_state.update({'page': 'main'}))
        st.info(f"صفحة {st.session_state.page} جاهزة للتعديل")
