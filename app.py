import streamlit as st

st.title("⚖️ المستشار القانوني الذكي")

# قاعدة البيانات المباشرة (هنا تضع المواد القانونية)
law_database = {
    "منحة قطع المعاش": "بناءً على المادة (10) من القانون 148 لسنة 2019: لا تستحق منحة قطع المعاش إذا توفى المستحق قبل تاريخ الصرف.",
    "عجز": "المادة (20): يُعتبر العجز غير مؤمن عليه إذا لم تتوافر شروط المدة التأمينية المقررة."
}

question = st.text_area("اطرح استفسارك:")

if st.button("تحليل"):
    found = False
    for key, value in law_database.items():
        if key in question:
            st.success("النتيجة المستخرجة من السجلات:")
            st.write(value)
            found = True
            break
    
    if not found:
        st.warning("عذراً، لم أجد مادة قانونية مطابقة لهذا الاستفسار في قاعدة البيانات.")

st.sidebar.write("مع تحيات وليد حماد")
st.sidebar.write("الإدارة العامة للشئون القانونية")
