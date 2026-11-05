# ถ้าอาจารย์ให้ไฟล์ zip มา

ส่วนใหญ่ zip คือ **ตัวเว็บที่ต้องรันบนเครื่องเราเอง** สิ่งที่เปลี่ยนมีแค่ "เว็บอยู่ที่ไหน"
ขั้นตอนอื่นทำตาม EXAM-STEPS.md เหมือนเดิม

> ใช้ Terminal **2 หน้าต่าง**: หน้าต่างแรกรันเว็บ (ห้ามปิด) หน้าต่างที่สองรันเทสต์
> ใน VS Code กดปุ่ม **+** ที่แถบ Terminal เพื่อเปิดหน้าต่างใหม่

---

## 1. แตก zip แล้วดูข้างใน

คลิกขวา → **Extract All** แตกไว้ที่ Desktop **แยกจาก** โฟลเดอร์โค้ดเทสต์ของเรา

| ข้างในมี | แปลว่า | ไปข้อ |
| --- | --- | --- |
| `index.html`, `.css`, `.js` (ไม่มี `package.json`) | เว็บธรรมดา (static) | 2A |
| `package.json` | เว็บ Node (React / Vite / Express) | 2B |
| `README` หรือไฟล์คำสั่งของอาจารย์ | อาจารย์บอกวิธีรันไว้แล้ว | **ทำตามของอาจารย์ก่อนเสมอ** |
| Excel template / โค้ดตั้งต้นของอาจารย์ | อาจารย์อยากให้ใช้ format ของเขา | ใช้ของอาจารย์ แล้วเอาวิธีคิดจากชุดนี้ไปเติม |

## 2A. เว็บธรรมดา (มี index.html)

Terminal หน้าต่างที่ 1 → เข้าโฟลเดอร์ที่มี `index.html`
```
cd Desktop\ชื่อโฟลเดอร์เว็บ
```
```
py -m http.server 8000
```
เปิดเบราว์เซอร์ไปที่ `http://localhost:8000` ต้องเห็นเว็บ

- **ไม่ควร** ดับเบิลคลิก `index.html` แล้วใช้ที่อยู่แบบ `file:///C:/...` เพราะบางเว็บทำงานไม่ครบ และโค้ดเราต่อ URL แบบ `base_url + "/"` ซึ่งใช้กับ `file://` ไม่ได้
- ถ้า port 8000 ถูกใช้แล้ว เปลี่ยนเป็น `py -m http.server 8080`

## 2B. เว็บ Node (มี package.json)

Terminal หน้าต่างที่ 1 → เข้าโฟลเดอร์ที่มี `package.json`
```
cd Desktop\ชื่อโฟลเดอร์เว็บ
```
```
npm install
```
```
npm start
```
- ถ้า `npm start` ใช้ไม่ได้ เปิด `package.json` ดูส่วน `"scripts"` แล้วใช้คำสั่งที่มี เช่น `npm run dev`
- ดู URL ที่ Terminal บอก เช่น `http://localhost:5173` หรือ `http://localhost:3000`
- ถ้าต้องใช้ database ให้ดู README ของอาจารย์ (เช่น `npx prisma db push`)

## 3. เปลี่ยน URL ในโค้ดเทสต์ (แก้จุดเดียว)

| เครื่องมือ | ไฟล์ | แก้เป็น |
| --- | --- | --- |
| Selenium / Playwright | `templates/python/conftest.py` | `BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")` |
| Robot | `templates/robot/config.yaml` | `url: "http://localhost:8000"` |
| Cypress | `cypress.config.js` | `baseUrl: 'http://localhost:8000'` |

ใช้เลข port ที่เว็บขึ้นจริง แล้ว Terminal หน้าต่างที่ 2 รันเทสต์ตามปกติ

## 4. ข้อดีของการได้ zip: อ่าน source code ได้

ไม่ต้องลองทำผิดทีละช่องเพื่อหาข้อความ error ให้ค้นจากโค้ดของเว็บเลย

1. VS Code → **File → Open Folder** → โฟลเดอร์เว็บของอาจารย์ (เปิดเป็นหน้าต่างใหม่ได้)
2. กด **Ctrl+Shift+F** แล้วค้นคำเหล่านี้

| ค้นคำว่า | จะเจอ |
| --- | --- |
| `required`, `error`, `invalid` | ข้อความ error ทุกอัน (ก๊อปไปใส่ expected_result ใน Excel) |
| `id="`, `data-test`, `name="` | locator ของทุกช่อง/ปุ่ม |
| `alert(`, `confirm(` | popup ที่ต้องจัดการในเทสต์ |
| `0.07`, `0.08`, `tax`, `discount`, `total` | สูตรคำนวณที่ต้องตรวจ |
| `password`, `user`, `admin` | user/รหัสผ่านที่ใช้ login ได้ |

## 5. ส่งงาน

- **ไม่ต้องส่งเว็บของอาจารย์คืน** ส่งแค่โค้ดเทสต์ของเรา + Excel
- **ห้ามแก้โค้ดเว็บของอาจารย์เพื่อให้เทสต์ผ่าน** ถ้าเว็บทำงานผิดจริง ให้เทสต์ **Fail**
  แล้วเขียนอธิบายใน Excel คอลัมน์ Actual Result (เจอบั๊ก = ทดสอบได้ดี)

## Error ที่เจอบ่อย

| อาการ | วิธีแก้ |
| --- | --- |
| เทสต์ fail ทุกตัว `ERR_CONNECTION_REFUSED` | เว็บไม่ได้รันอยู่ / ปิด Terminal หน้าต่างที่ 1 ไป / port ผิด |
| `npm` is not recognized | เครื่องไม่มี Node.js ต้องติดตั้งก่อน |
| `npm install` error | ลบโฟลเดอร์ `node_modules` กับ `package-lock.json` แล้ว `npm install` ใหม่ |
| `Address already in use` | port ถูกใช้แล้ว เปลี่ยนเลข port หรือปิด server ตัวเก่า (Ctrl+C) |
| เปิดเว็บได้แต่หน้าขาว | ใช้ `file://` อยู่ ให้เปิดผ่าน `http://localhost:...` แทน |
