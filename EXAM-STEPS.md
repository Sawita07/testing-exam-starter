# ขั้นตอนตอนสอบ (ทำตามลำดับ)

> พิมพ์คำสั่งใน Terminal **ทีละบรรทัด** แล้วกด Enter ทีละครั้ง
> หลักสำคัญที่สุด: **ทำให้รันผ่าน 1 เคสก่อน แล้วค่อยเพิ่ม** อย่าเขียนยาวทีเดียวแล้วค่อยรัน

## 0. เช็กเครื่อง (2 นาที)
```
py --version
```
```
py -m pip --version
```
```
git --version
```
ขึ้นเลขเวอร์ชันทั้งหมด = พร้อม และต้องมี Google Chrome ในเครื่อง
(ถ้า `py` ใช้ไม่ได้ ให้ใช้ `python` แทนทุกที่)

## 1. Clone โค้ดมา
```
cd Desktop
```
```
git clone https://github.com/Sawita07/testing-exam-starter.git 67160453
```
(เปลี่ยน `67160453` เป็นชื่อโฟลเดอร์ที่อาจารย์สั่ง)

## 2. เปิดโฟลเดอร์
VS Code → **File → Open Folder** → เลือกโฟลเดอร์ `67160453`
เปิด Terminal ด้วย **Ctrl + `**

## 3. ติดตั้ง package (5-10 นาที ทำระหว่างอ่านโจทย์ได้)
```
py -m pip install -r requirements.txt
```
```
py -m playwright install chromium
```
(ใช้แค่ Selenium หรือ Robot ไม่ต้องรันบรรทัด playwright)

## 4. ลองรัน starter ก่อนแก้อะไร (เช็กว่าเครื่องพร้อม)
```
cd templates\python
```
```
py -m pytest test_selenium_starter.py -v
```
ต้องขึ้น `5 passed` ถ้าไม่ผ่าน ดูตาราง Error ใน README.md ข้อ 3

## 5. อ่านโจทย์ + ลองเล่นเว็บด้วยมือ (10 นาที)
1. อ่านโจทย์ ขีดเส้นใต้ทุกจุดที่ต้อง **ตรวจ (assert)** เช่น ข้อความ, URL, จำนวน, ราคา
2. เปิดเว็บด้วยมือ ทำตาม flow ในโจทย์ 1 รอบ
3. ลองทำผิดดูทุกช่อง (เว้นว่าง, รหัสผิด) แล้ว **จดข้อความ error ทุกอันแบบตัวต่อตัว**
4. กด **F12** หา locator ของทุกช่องและปุ่ม แล้วจดลงตารางนี้

```
ชื่อที่ตั้งเอง      | locator                          | ใช้ทำอะไร
username           | [data-test="username"]           | พิมพ์
login_button       | [data-test="login-button"]       | คลิก
error              | [data-test="error"]              | อ่านข้อความ error
_____________      | ______________________________   | __________
```
ลำดับการเลือก locator: `data-test` / `id` → `name` → CSS class → XPath
ทดสอบ locator ใน F12 → Console:
```
$$('[data-test="username"]')
```
```
$x('//button[text()="Login"]')
```
ได้ 1 ตัว = ใช้ได้ / ได้ 0 = ผิด / ได้หลายตัว = ต้องเจาะจงกว่านี้

## 6. เขียน Excel (20 นาที)
เปิด `templates/testdata/testdata.xlsx` (วิธีคิดเคสดูที่ **TEST-DESIGN-GUIDE.md**)
1. ชีท **TestCases**: TC ID, Scenario, ชื่อเคส, Positive/Negative, Pre-condition, Steps, Expected
2. ชีท **TestData**: 1 แถว = 1 เคส แถวแรกเป็นชื่อคอลัมน์ ซึ่งโค้ดใช้เป็น key (`row["username"]`)
   - ถ้าเว็บมีช่องกรอกอื่น ให้เพิ่มคอลัมน์ใหม่ได้เลย เช่น `email`, `phone`
   - ตั้ง format เป็น **Text** ทั้งชีท
3. **Save แล้วปิด Excel** ก่อนรันโค้ด

## 7. เขียนโค้ด (ส่วนใหญ่ของเวลา)
ทำตาม **EDIT-GUIDE.md**
1. แก้กล่อง LOCATORS ด้านบนไฟล์
2. เขียน `test_..._success` แบบข้อมูลตายตัวให้ผ่านก่อน
3. รัน (ใช้ `-k` รันเฉพาะเทสต์ที่กำลังทำ)
```
py -m pytest test_selenium_starter.py -k success -v
```
4. ผ่านแล้วค่อยทำเวอร์ชันอ่าน Excel ให้ครอบคลุม negative
5. ถ้าเคสไหนทำไม่ทัน อย่าลบทิ้ง ใส่ `@pytest.mark.skip(reason="...")` ไว้ แล้วไปทำเคสอื่นต่อ

## 8. รันรอบสุดท้าย + เก็บหลักฐาน
```
py -m pytest -v --html=report.html
```
(Robot: `py -m robot ไฟล์.robot` จะได้ `report.html`, `log.html` อัตโนมัติ)

กลับไปกรอก Excel ชีท TestCases: คอลัมน์ **Actual Result** และ **Status** (Pass/Fail)
- ถ้าเว็บทำงานไม่ตรงโจทย์จริง (bug) ให้เทสต์ **Fail** ได้ และเขียนอธิบายใน Actual Result

## 9. ส่งงาน
- ไฟล์โค้ด (`.py` หรือ `.robot` พร้อม `config.yaml`) + ไฟล์ Excel
- ตั้งชื่อตามที่อาจารย์สั่ง (มักเป็นรหัสนิสิต)
- ถ้าต้องส่งหลายไฟล์ ให้คลิกขวาโฟลเดอร์ → Compress to ZIP (ไม่ต้องใส่ `__pycache__`, `node_modules`)

---

## ถ้าติด
| ติดตรงไหน | ทำอะไร |
| --- | --- |
| หา element ไม่เจอ | F12 เช็ก locator ใน Console / เพิ่มการรอ / ดูว่าอยู่ใน iframe ไหม |
| ไม่รู้คำสั่ง | เปิด **CHEATSHEET.md** หรือเปิดไฟล์ใน `examples/saucedemo` ที่ทำคล้าย ๆ กัน |
| รันแล้วผ่านบ้างตกบ้าง | หลังกดเปลี่ยนหน้า ให้รอ URL ก่อนอ่านค่าเสมอ |
| เวลาใกล้หมด | ส่งที่รันผ่านแล้วก่อน + Excel ที่ออกแบบครบ (Excel ได้คะแนนแยก) |
