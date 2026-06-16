from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>نظام إدارة الشؤون القانونية - منطقة البحيرة</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family:'Cairo',Tahoma,sans-serif; }
body { background:#f5f7fa; color:#333; padding:20px; }
.container { max-width:1400px; margin:auto; background:#fff; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.1); padding:25px; }
.header { text-align:center; border-bottom:3px solid #0d47a1; padding-bottom:15px; margin-bottom:25px; }
.header h1 { color:#0d47a1; font-size:22px; margin-bottom:5px; }
.header h2 { color:#1565c0; font-size:18px; font-weight:normal; }
.nav { display:flex; flex-wrap:wrap; gap:10px; margin-bottom:25px; border-bottom:2px solid #e0e0e0; padding-bottom:15px; }
.nav button { padding:12px 20px; background:#e3f2fd; border:none; border-radius:8px; cursor:pointer; font-size:15px; font-weight:bold; color:#0d47a1; transition:0.3s; }
.nav button.active, .nav button:hover { background:#0d47a1; color:#fff; }
.section { display:none; }
.section.active { display:block; }
.filter-box { background:#e3f2fd; padding:15px; border-radius:8px; margin-bottom:20px; display:flex; flex-wrap:wrap; gap:12px; align-items:end; }
.filter-box label { font-weight:bold; font-size:14px; }
.filter-box input, .filter-box select { padding:8px 10px; border:1px solid #90caf9; border-radius:6px; font-size:14px; }
.btn { padding:10px 18px; background:#1976d2; color:#fff; border:none; border-radius:6px; cursor:pointer; font-weight:bold; transition:0.3s; }
.btn:hover { background:#0d47a1; }
.btn-success { background:#2e7d32; }
.btn-success:hover { background:#1b5e20; }
.btn-warning { background:#f57c00; }
.btn-warning:hover { background:#e65100; }
.table-wrapper { overflow-x:auto; }
table { width:100%; border-collapse:collapse; margin-top:15px; }
th { background:#0d47a1; color:#fff; padding:12px 8px; text-align:center; font-size:14px; border:1px solid #1565c0; }
td { padding:10px 8px; text-align:center; border:1px solid #ddd; font-size:13px; }
tr:nth-child(even) { background:#f8f9fa; }
.actions { display:flex; gap:6px; justify-content:center; flex-wrap:wrap; }
.action-btn { padding:6px 10px; font-size:12px; border:none; border-radius:5px; cursor:pointer; color:#fff; }
.open { background:#1976d2; }
.pdf { background:#d32f2f; }
.word { background:#2b5797; }
.print { background:#6a1b9a; }
.modal { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; align-items:center; justify-content:center; }
.modal-content { background:#fff; padding:25px; border-radius:12px; width:90%; max-width:700px; max-height:85vh; overflow-y:auto; }
.modal h3 { color:#0d47a1; margin-bottom:15px; border-bottom:2px solid #e0e0e0; padding-bottom:10px; }
.form-group { margin-bottom:15px; }
.form-group label { display:block; margin-bottom:6px; font-weight:bold; }
.form-group input, .form-group textarea, .form-group select { width:100%; padding:10px; border:1px solid #ccc; border-radius:6px; }
.close-btn { float:left; font-size:28px; cursor:pointer; color:#999; }
.close-btn:hover { color:#000; }
.footer-sign { margin-top:30px; text-align:center; border-top:2px solid #0d47a1; padding-top:20px; }
.footer-sign p { margin:8px 0; font-weight:bold; }
.bayan-header { text-align:center; margin:20px 0; padding:15px; background:#e3f2fd; border-radius:8px; }
.bayan-header select { padding:8px 15px; font-size:16px; font-weight:bold; }
.search-box { background:#fff3e0; padding:20px; border-radius:8px; margin-bottom:20px; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>الهيئة القومية للتأمين الاجتماعي - الإدارة العامة للشؤون القانونية</h1>
    <h2>ديوان عام منطقة: البحيرة</h2>
  </div>

  <div class="nav">
    <button class="active" onclick="showSection('reports')">التقارير</button>
    <button onclick="showSection('archive')">الأرشيف</button>
    <button onclick="showSection('deleted')">القضايا المحذوفة</button>
    <button onclick="showSection('search')">البحث عن دعوى</button>
  </div>

  <div id="reports" class="section active">
    <div class="bayan-header">
      <label>بيان </label>
      <select id="bayanType" onchange="changeBayan()">
        <option value="qadaya">بالقضايا</option>
        <option value="ahkam">بالأحكام</option>
      </select>
    </div>

    <div class="filter-box">
      <div><label>اسم المنطقة:</label><input type="text" id="manteqa" value="البحيرة"></div>
      <div><label>اسم الأستاذ:</label><input type="text" id="ostaz" value="وليد شعبان حماد"></div>
      <div><label>من تاريخ:</label><input type="date" id="fromDate"></div>
      <div><label>إلى تاريخ:</label><input type="date" id="toDate"></div>
      <button class="btn" onclick="loadReport()">عرض التقرير</button>
    </div>

    <div id="reportTitle" style="text-align:center; font-size:18px; font-weight:bold; margin:15px 0;"></div>
    
    <div class="table-wrapper">
      <table id="reportTable">
        <thead id="tableHead"></thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>

    <div class="actions" style="margin-top:20px;">
      <button class="btn open" onclick="openReport()">فتح التقرير</button>
      <button class="btn pdf" onclick="downloadPDF()">تحميل PDF</button>
      <button class="btn word" onclick="downloadWord()">تحميل Word</button>
      <button class="btn print" onclick="printReport()">طباعة التقرير</button>
    </div>

    <div class="bayan-header">
      <h3>استخراج صور أحكام</h3>
      <div style="margin:10px 0;">
        <select id="ahkamType">
          <option>للصالح والضد</option>
          <option>للصالح</option>
          <option>للضد</option>
        </select>
        من <input type="date" id="ahkamFrom"> حتى <input type="date" id="ahkamTo">
        <button class="btn btn-success" onclick="extractAhkam()">استخراج</button>
      </div>
      <div id="ahkamResults"></div>
      <button class="btn word" onclick="downloadAllAhkamWord()">تحميل كل الأحكام Word</button>
    </div>

    <div class="footer-sign">
      <p>وتفضلوا سيادتكم بقبول وافر الاحترام والتقدير</p>
      <p>عضو الإدارة / مدير الإدارة</p>
    </div>
  </div>

  <div id="archive" class="section">
    <h3 style="margin-bottom:15px; color:#0d47a1;">أرشيف الأحكام المحكوم فيها</h3>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>م</th><th>رقم الدعوى</th><th>السنة</th><th>المحكمة</th><th>الخصوم</th>
            <th>موضوع الدعوى</th><th>تاريخ الحكم</th><th>المنطوق</th><th>النتيجة</th><th>الإجراء</th>
          </tr>
        </thead>
        <tbody id="archiveBody"></tbody>
      </table>
    </div>
  </div>

  <div id="deleted" class="section">
    <h3 style="margin-bottom:15px; color:#d32f2f;">القضايا المحذوفة</h3>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>م</th><th>رقم الدعوى</th><th>السنة</th><th>المحكمة</th><th>الخصوم</th>
            <th>موضوع الدعوى</th><th>تاريخ الحذف</th><th>سبب الحذف</th><th>عرض</th>
          </tr>
        </thead>
        <tbody id="deletedBody"></tbody>
      </table>
    </div>
  </div>

  <div id="search" class="section">
    <div class="search-box">
      <h3 style="margin-bottom:15px; color:#0d47a1;">البحث عن دعوى</h3>
      <div class="filter-box">
        <div><label>الاسم:</label><input type="text" id="searchName"></div>
        <div><label>رقم الدعوى/الاستئناف/الطعن:</label><input type="text" id="searchNumber"></div>
        <div><label>السنة:</label><input type="number" id="searchYear"></div>
        <button class="btn" onclick="searchCase()">بحث</button>
      </div>
    </div>
    <div id="searchResult"></div>
  </div>
</div>

<div id="actionModal" class="modal">
  <div class="modal-content">
    <span class="close-btn" onclick="closeModal()">&times;</span>
    <h3>إضافة الإجراء المتخذ</h3>
    <div class="form-group">
      <label><input type="radio" name="ejra" value="taan" onchange="showEjraForm()"> تم الطعن</label>
      <label><input type="radio" name="ejra" value="hifz" onchange="showEjraForm()"> حفظ</label>
    </div>
    <div id="ejraForm"></div>
  </div>
</div>

<div id="deletedModal" class="modal">
  <div class="modal-content">
    <span class="close-btn" onclick="closeDeletedModal()">&times;</span>
    <h3>بيانات القضية المحذوفة</h3>
    <div id="deletedDetails"></div>
  </div>
</div>

<script>
let currentBayan = 'qadaya';
let currentCaseId = null;

function showSection(id) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  event.target.classList.add('active');
}

function changeBayan() {
  currentBayan = document.getElementById('bayanType').value;
  loadReport();
}

function loadReport() {
  const ostaz = document.getElementById('ostaz').value;
  const from = document.getElementById('fromDate').value;
  const to = document.getElementById('toDate').value;
  const ahkamType = document.getElementById('ahkamType') ? document.getElementById('ahkamType').value : 'للصالح والضد';
  
  if(currentBayan === 'qadaya') {
    document.getElementById('reportTitle').innerText = `كشف بالدعاوى المتداولة خلال الفترة من ${from} حتى ${to} طرف الأستاذ / ${ostaz}`;
    document.getElementById('tableHead').innerHTML = `
      <tr>
        <th>م</th><th>رقم الدعوى</th><th>اباستيناف</th><th>ابطعن</th><th>حسب الحالة</th>
        <th>السنة القضائية</th><th>الدائرة</th><th>النوع</th><th>المحكمة</th><th>اسم المحكمة</th>
        <th>المأمورية</th><th>أسماء الخصوم</th><th>موضوع الدعوى</th><th>الاستئناف</th><th>الطعن</th><th>آخر إجراء</th>
      </tr>`;
    document.getElementById('tableBody').innerHTML = `
      <tr><td>1</td><td>123</td><td>-</td><td>-</td><td>متداولة</td><td>2025</td><td>3</td><td>مدني</td>
      <td>ابتدائية</td><td>محكمة دمنهور</td><td>مسجلة</td><td>أحمد ضد الهيئة</td><td>مطالبة</td><td>-</td><td>-</td>
      <td>جلسة 12/5/2026 للاطلاع</td></tr>`;
  } else {
    document.getElementById('reportTitle').innerText = `بيان بالأحكام ${ahkamType} خلال الفترة من ${from} حتى ${to} طرف الأستاذ / ${ostaz}`;
    document.getElementById('tableHead').innerHTML = `
      <tr>
        <th>م</th><th>رقم الدعوى</th><th>اباستيناف</th><th>ابطعن</th><th>حسب الحالة</th>
        <th>السنة القضائية</th><th>الدائرة</th><th>النوع</th><th>المحكمة</th><th>اسم المحكمة</th>
        <th>المأمورية</th><th>أسماء الخصوم</th><th>موضوع الدعوى</th><th>الاستئناف</th><th>الطعن</th>
        <th>تاريخ الحكم</th><th>منطوق الحكم</th><th>الصالح/الضد</th>
      </tr>`;
    document.getElementById('tableBody').innerHTML = `
      <tr><td>1</td><td>456</td><td>-</td><td>-</td><td>محكوم</td><td>2024</td><td>2</td><td>عمال</td>
      <td>ابتدائية</td><td>محكمة كفر الدوار</td><td>مسجلة</td><td>محمد ضد الهيئة</td><td>تعويض</td><td>-</td><td>-</td>
      <td>10/3/2026</td><td>قبول الدعوى</td><td>الصالح</td></tr>`;
  }
}

function openReport() { alert('فتح التقرير في نافذة جديدة'); }
function downloadPDF() { alert('تحميل ملف PDF'); }
function downloadWord() { alert('تحميل ملف Word'); }
function printReport() { window.print(); }

function extractAhkam() {
  const type = document.getElementById('ahkamType').value;
  const from = document.getElementById('ahkamFrom').value;
  const to = document.getElementById('ahkamTo').value;
  document.getElementById('ahkamResults').innerHTML = `
    <table style="width:100%; margin-top:15px;">
      <tr><th>رقم الدعوى</th><th>بيانات الحصر الخارجي</th><th>تاريخ الحكم</th><th>المنطوق</th><th>إجراءات</th></tr>
      <tr><td>789</td><td>أحمد ضد الهيئة - مدني</td><td>15/4/2026</td><td>رفض الدعوى</td>
      <td class="actions"><button class="action-btn open">فتح</button><button class="action-btn pdf">PDF</button><button class="action-btn print">طباعة</button></td></tr>
    </table>`;
}

function downloadAllAhkamWord() { alert('تحميل كل الأحكام في ملف Word مرتبة'); }

document.getElementById('archiveBody').innerHTML = `
  <tr><td>1</td><td>456</td><td>2024</td><td>ابتدائية</td><td>محمد ضد الهيئة</td><td>تعويض</td><td>10/3/2026</td><td>قبول</td><td>الصالح</td>
  <td><button class="btn btn-warning" onclick="openActionModal(1)">إضافة الإجراء</button></td></tr>`;

function openActionModal(id) {
  currentCaseId = id;
  document.getElementById('actionModal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('actionModal').style.display = 'none';
  document.getElementById('ejraForm').innerHTML = '';
}

function showEjraForm() {
  const val = document.querySelector('input[name="ejra"]:checked').value;
  if(val === 'taan') {
    document.getElementById('ejraForm').innerHTML = `
      <div class="form-group"><label>رقم الطعن:</label><input type="text" id="taanNum"></div>
      <div class="form-group"><label>بيانات الطعن:</label><textarea id="taanData"></textarea></div>
      <button class="btn btn-success" onclick="saveTaanArchive()">حفظ للأرشيف</button>
      <button class="btn" onclick="addTaanQadaya()">إضافة للقضايا المتداولة</button>`;
  } else {
    document.getElementById('ejraForm').innerHTML = `
      <div class="form-group"><label>بيانات مذكرة أسباب الحفظ:</label><textarea id="hifzData"></textarea></div>
      <button class="btn btn-success" onclick="saveHifz()">حفظ</button>`;
  }
}

function saveTaanArchive() { alert('تم حفظ الطعن في الأرشيف - رقم الطعن لا يظهر في تقارير الأحكام'); closeModal(); }
function addTaanQadaya() { alert('تم إضافة الطعن للقضايا المتداولة برقم '+document.getElementById('taanNum').value); closeModal(); }
function saveHifz() { alert('تم حفظ بيانات المذكرة - لا تظهر في تقارير الأحكام'); closeModal(); }

document.getElementById('deletedBody').innerHTML = `
  <tr><td>1</td><td>999</td><td>2023</td><td>ابتدائية</td><td>سعيد ضد الهيئة</td><td>مطالبة</td><td>1/1/2026</td><td>تصالح</td>
  <td><button class="btn open" onclick="openDeleted(1)">فتح القضية</button></td></tr>`;

function openDeleted(id) {
  document.getElementById('deletedDetails').innerHTML = `
    <p><b>رقم الدعوى:</b> 999 لسنة 2023</p>
    <p><b>الخصوم:</b> سعيد ضد الهيئة</p>
    <p><b>الموضوع:</b> مطالبة</p>
    <p><b>المحكمة:</b> محكمة دمنهور الابتدائية</p>
    <p><b>تاريخ الحذف:</b> 1/1/2026</p>
    <p><b>سبب الحذف:</b> تم التصالح بين الطرفين</p>
    <p><b>جميع البيانات حتى تاريخ الحذف:</b> ...</p>`;
  document.getElementById('deletedModal').style.display = 'flex';
}

function closeDeletedModal() {
  document.getElementById('deletedModal').style.display = 'none';
}

function searchCase() {
  const name = document.getElementById('searchName').value;
  const num = document.getElementById('searchNumber').value;
  const year = document.getElementById('searchYear').value;
  document.getElementById('searchResult').innerHTML = `
    <table style="width:100%; margin-top:20px;">
      <tr><th>رقم الدعوى</th><th>السنة</th><th>الخصوم</th><th>الموضوع</th><th>المحكمة</th><th>عرض</th></tr>
      <tr><td>${num || '123'}</td><td>${year || '2025'}</td><td>${name || 'أحمد'} ضد الهيئة</td><td>مطالبة</td><td>دمنهور</td>
      <td><button class="btn open" onclick="alert('فتح الدعوى/الاستئناف/الطعن بكل بياناتها')">فتح</button></td></tr>
    </table>`;
}

loadReport();
</script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
