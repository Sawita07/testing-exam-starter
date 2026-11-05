# ชุดเริ่มต้นสอบ: Automated Web Testing (Selenium / Playwright / Robot Framework)

ชุดนี้ใช้สำหรับสอบปฏิบัติวิชา Software Testing and QA (88833965) โจทย์คืออาจารย์ให้เว็บมา
เราต้องออกแบบ **Test Case + Test Data ใน Excel** แล้วเขียนโค้ดทดสอบ จากนั้นส่งไฟล์ Excel กับโค้ด

| ไฟล์ | ใช้ทำอะไร |
| --- | --- |
| **EXAM-STEPS.md** | ขั้นตอนตอนสอบ ทำตามลำดับ ตั้งแต่เปิดเครื่องจนส่งงาน |
| **TEST-DESIGN-GUIDE.md** | วิธีคิด test case และ test data ให้ครบ (ส่วนที่ได้คะแนนใน Excel) |
| **EDIT-GUIDE.md** | วิธีแก้ starter ให้ใช้กับเว็บของข้อสอบ |
| **CHEATSHEET.md** | คำสั่งของแต่ละเครื่องมือเทียบกัน (เปิดเว็บ / พิมพ์ / คลิก / assert / รอ) |
| `templates/` | **โค้ดตั้งต้นสำหรับวันสอบ** ก๊อปไปแก้ได้เลย |
| `examples/saucedemo/` | การบ้านทุกชิ้นที่ทำเสร็จแล้ว ใช้เปิดเทียบ |

> สอบเปิดเน็ตแต่ห้ามใช้ AI: **ถามอาจารย์ก่อนว่าเปิด repo ที่เตรียมเองได้ไหม**
> และต้องเข้าใจทุกบรรทัดจนเขียนเองได้ เพราะเว็บในข้อสอบอาจไม่ใช่ saucedemo

---

## 0. ภาพรวม (อ่าน 1 นาที)

```
templates/
├── testdata/testdata.xlsx        ← Excel 2 ชีท: TestCases (ออกแบบ) + TestData (โค้ดอ่าน)
├── python/
│   ├── conftest.py               ← เปิด/ปิด Chrome + อ่าน Excel (ไม่ต้องแก้)
│   ├── test_selenium_starter.py  ← แก้กล่อง LOCATORS + ขั้นตอน
│   └── test_playwright_starter.py
└── robot/
    ├── config.yaml               ← url, user, path ของ Excel
    └── starter.robot             ← แก้ Variables (locator) + Test Cases

examples/saucedemo/               ← คำตอบการบ้านทุกชิ้น (ผ่านการรันจริงแล้ว)
├── python_tests/                 ← Selenium + Playwright: ซื้อ 1 ชิ้น, sort+tax, data-driven
├── robot/                        ← E2E YAML+Excel (Scenario 1,2) และ sort+tax
├── cypress_tests/                ← Cypress sort+tax
└── testdata/testdata.xlsx        ← test case 8 ข้อ (positive 2 + negative 6)
```

ทุก starter ทำงานเหมือนกัน คือ **Login แบบตายตัว 1 เคส + Login จาก Excel 4 เคส** รันผ่านได้ทันที
ตอนสอบให้เปลี่ยน locator กับขั้นตอนเป็นของเว็บข้อสอบ (ดู EDIT-GUIDE.md)

## 1. ติดตั้งครั้งเดียว (ทำที่บ้านก่อนสอบ)

ต้องมี Python และ Google Chrome ก่อน (ตอนติดตั้ง Python ติ๊ก **Add Python to PATH**)

```
py -m pip install -r requirements.txt
```
```
py -m playwright install chromium
```

ถ้าจะใช้ Cypress ต้องมี Node.js ด้วย แล้วรันในโฟลเดอร์ `examples/saucedemo/cypress_tests`

```
npm install
```

## 2. วิธีรัน

**Selenium / Playwright** (อยู่ในโฟลเดอร์ `templates/python`)
```
py -m pytest test_selenium_starter.py -v
```
```
py -m pytest test_playwright_starter.py --headed -v
```

**Robot Framework** (อยู่ในโฟลเดอร์ `templates/robot`)
```
py -m robot starter.robot
```
ผลอยู่ใน `report.html` กับ `log.html` (ดับเบิลคลิกเปิดในเบราว์เซอร์)

**รันตัวอย่าง saucedemo ทั้งหมด** (อยู่ในโฟลเดอร์ `examples/saucedemo`)
```
py -m pytest python_tests -v
```
```
cd robot
py -m robot tests
```

## 3. Error ที่เจอบ่อย

| อาการ | สาเหตุ / วิธีแก้ |
| --- | --- |
| `'py' is not recognized` | ใช้ `python` แทน `py` หรือติดตั้ง Python ใหม่แล้วติ๊ก Add to PATH |
| `ModuleNotFoundError: No module named 'selenium'` | ยังไม่ได้ `py -m pip install -r requirements.txt` |
| `fixture 'page' not found` | ยังไม่ได้ลง `pytest-playwright` |
| `Executable doesn't exist ... playwright` | ยังไม่ได้รัน `py -m playwright install chromium` |
| `SessionNotCreatedException` / version ไม่ตรง | Chrome กับ chromedriver ไม่ตรงกัน: อัปเดต Chrome แล้ว `py -m pip install -U selenium` |
| `NoSuchElementException` / `TimeoutException` | locator ผิด ไปเช็กด้วย F12 → Console พิมพ์ `$$('[data-test="xxx"]')` หรือ `$x('//xpath')` |
| `ElementClickInterceptedException` | มี popup บังปุ่ม (เช่น popup รหัสผ่านของ Chrome ซึ่งปิดไว้แล้วใน starter) หรือต้องเลื่อนจอ |
| เทสต์ผ่านบ้างตกบ้าง (flaky) | อ่านค่าก่อนหน้าเว็บเปลี่ยนเสร็จ: หลังกดเปลี่ยนหน้าให้ **รอ URL** ก่อนเสมอ |
| เลขไม่เท่ากันทั้งที่ดูเหมือนเท่า | เว็บแสดง `57.980000000000004` ได้จริง ต้อง `round(x, 2)` ทั้งสองฝั่ง |
| `No keyword with name 'Open Workbook'` | ยังไม่ได้ `pip install rpaframework` หรือลืม `Library  RPA.Excel.Files` |
| `No keyword with name 'Normalize Path'` | ลืม `Library  OperatingSystem` |
| Robot หาไฟล์ Excel/YAML ไม่เจอ | path นับจากโฟลเดอร์ที่ไฟล์ `.robot` อยู่ (`${CURDIR}`) ไม่ใช่จากที่พิมพ์คำสั่ง |
| เปิด Excel ค้างไว้แล้วโค้ดอ่านไม่ได้ / `PermissionError` | ปิด Excel ก่อนรัน (หรือ Save แล้วปิด) |
| รหัสไปรษณีย์ `01234` กลายเป็น `1234` | ตั้ง format คอลัมน์ใน Excel เป็น **Text** |
