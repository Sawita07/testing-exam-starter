# คู่มือแก้ starter ให้ใช้กับเว็บของข้อสอบ

ตัวอย่างที่ทำเสร็จแล้ว เปิดเทียบได้ที่ `examples/saucedemo/`
เลือกเครื่องมือ **1 ตัว** ที่ถนัดที่สุด (ถ้าอาจารย์ไม่ได้กำหนด) แล้วก๊อปไฟล์จาก `templates/` ไปแก้

---

## วิธีคิด: ทุกเทสต์มี 4 ท่อนเสมอ

```
1. เตรียม   (Arrange)  เปิดเว็บ, login, ไปหน้าที่ต้องการ
2. ทำ      (Act)      พิมพ์, คลิก, เลือก ตามโจทย์
3. รอ      (Wait)     รอให้หน้าเปลี่ยน / element โผล่  ← ลืมบ่อยที่สุด
4. ตรวจ    (Assert)   เทียบผลจริงกับ expected
```

เขียนขั้นตอนโจทย์เป็นภาษาคนก่อน 1 บรรทัดต่อ 1 action แล้วค่อยแปลงเป็นโค้ดทีละบรรทัด

```
# เปิดเว็บ
# กรอก username = standard_user
# กรอก password = secret_sauce
# คลิก Login
# รอ URL มีคำว่า inventory
# ตรวจหัวข้อ = Products
```

---

## ขั้น A: แก้กล่อง LOCATORS ด้านบนไฟล์

ตั้งชื่อเองให้อ่านรู้เรื่อง แล้วใส่ locator ที่จดจาก F12

| เครื่องมือ | เขียนแบบนี้ |
| --- | --- |
| Selenium | `"email": (By.ID, "email"),` |
| Playwright | `"email": "#email",` |
| Robot | `${EMAIL_INPUT}    id:email` |

**แปลง locator ระหว่างเครื่องมือ**

| HTML ที่เห็นใน F12 | Selenium | Playwright | Robot |
| --- | --- | --- | --- |
| `id="email"` | `(By.ID, "email")` | `"#email"` | `id:email` |
| `name="email"` | `(By.NAME, "email")` | `'[name="email"]'` | `name:email` |
| `data-test="email"` | `(By.CSS_SELECTOR, '[data-test="email"]')` | `'[data-test="email"]'` | `css:[data-test="email"]` |
| `class="btn primary"` | `(By.CSS_SELECTOR, ".btn.primary")` | `".btn.primary"` | `css:.btn.primary` |
| ปุ่มที่มีคำว่า Save | `(By.XPATH, '//button[text()="Save"]')` | `'xpath=//button[text()="Save"]'` หรือ `"text=Save"` | `xpath://button[text()="Save"]` |
| ลิงก์ที่มีคำว่า Menu | `(By.XPATH, '//a[contains(text(),"Menu")]')` | `"text=Menu"` | `xpath://a[contains(text(),"Menu")]` |

---

## ขั้น B: แปลงภาษาคนเป็นโค้ด

ใช้ helper ใน starter (Selenium) / คำสั่งตรง (Playwright, Robot)

| ภาษาคน | Selenium (starter) | Playwright | Robot |
| --- | --- | --- | --- |
| เปิดเว็บ | `driver.get(base_url + "/")` | `page.goto(base_url + "/")` | `Go To    ${URL}` |
| พิมพ์ | `type_text(driver, "email", "a@b.com")` | `page.fill(L["email"], "a@b.com")` | `Input Text    ${EMAIL_INPUT}    a@b.com` |
| คลิก | `click(driver, "save")` | `page.click(L["save"])` | `Click Element    ${SAVE_BTN}` |
| เลือก dropdown | `select_by_text(driver, "sort", "Price (low to high)")` | `page.select_option(L["sort"], label="Price (low to high)")` | `Select From List By Label    ${SORT}    Price (low to high)` |
| ติ๊ก checkbox | `click(driver, "agree")` | `page.check(L["agree"])` | `Select Checkbox    ${AGREE}` |
| รอเปลี่ยนหน้า | `wait_url(driver, "cart")` | `expect(page).to_have_url(re.compile(".*cart"))` | `Wait Until Location Contains    cart` |
| อ่านข้อความ | `text_of(driver, "title")` | `page.inner_text(L["title"])` | `${t}=    Get Text    ${TITLE}` |
| ตรวจข้อความ | `assert text_of(driver, "title") == "Products"` | `expect(page.locator(L["title"])).to_have_text("Products")` | `Element Text Should Be    ${TITLE}    Products` |
| ตรวจว่ามีคำนี้ | `assert "Thank" in text_of(driver, "msg")` | `expect(page.locator(L["msg"])).to_contain_text("Thank")` | `Element Should Contain    ${MSG}    Thank` |
| ตรวจ URL | `assert driver.current_url == base_url + "/done"` | `expect(page).to_have_url(base_url + "/done")` | `Location Should Be    ${URL}/done` |
| นับจำนวน | `assert len(driver.find_elements(*L["item"])) == 2` | `expect(page.locator(L["item"])).to_have_count(2)` | `Page Should Contain Element    ${ITEM}    limit=2` |

ถ้าต้องเพิ่ม helper หรือคำสั่งอื่น ดู **CHEATSHEET.md**

---

## ขั้น C: เขียนเคสแบบตายตัวให้ผ่านก่อน

ตัวอย่าง: สมมติโจทย์คือ "สมัครสมาชิก กรอกชื่อ อีเมล ติ๊กยอมรับ กด Register แล้วต้องเห็น Welcome"

**Selenium**
```python
L = {
    "name":     (By.ID, "name"),
    "email":    (By.ID, "email"),
    "agree":    (By.ID, "agree"),
    "register": (By.XPATH, '//button[text()="Register"]'),
    "message":  (By.CSS_SELECTOR, ".alert"),
}

def test_register_success(driver, base_url):
    driver.get(base_url + "/register")              # 1 เตรียม
    type_text(driver, "name", "Somchai")            # 2 ทำ
    type_text(driver, "email", "somchai@test.com")
    click(driver, "agree")
    click(driver, "register")
    wait_url(driver, "welcome")                     # 3 รอ
    assert "Welcome" in text_of(driver, "message")  # 4 ตรวจ
```

**Playwright**
```python
L = {"name": "#name", "email": "#email", "agree": "#agree",
     "register": "text=Register", "message": ".alert"}

def test_register_success(page: Page, base_url):
    page.goto(base_url + "/register")
    page.fill(L["name"], "Somchai")
    page.fill(L["email"], "somchai@test.com")
    page.check(L["agree"])
    page.click(L["register"])
    expect(page).to_have_url(re.compile(".*welcome"))
    expect(page.locator(L["message"])).to_contain_text("Welcome")
```

**Robot**
```robotframework
*** Variables ***
${NAME_INPUT}      id:name
${EMAIL_INPUT}     id:email
${AGREE_BOX}       id:agree
${REGISTER_BTN}    xpath://button[text()="Register"]
${MESSAGE}         css:.alert

*** Test Cases ***
Register Success
    Go To    ${URL}/register
    Input Text    ${NAME_INPUT}     Somchai
    Input Text    ${EMAIL_INPUT}    somchai@test.com
    Select Checkbox    ${AGREE_BOX}
    Click Button    ${REGISTER_BTN}
    Wait Until Location Contains    welcome
    Element Should Contain    ${MESSAGE}    Welcome
```

---

## ขั้น D: เปลี่ยนเป็นอ่านข้อมูลจาก Excel

1. ในชีท TestData สร้างคอลัมน์ตามช่องที่ต้องกรอก เช่น `tc_id | run | name | email | agree | expected_result`
2. ในโค้ด แทนค่าตายตัวด้วย `row["ชื่อคอลัมน์"]` (Robot ใช้ `${row}[ชื่อคอลัมน์]`)
3. แยก positive/negative ด้วยการเช็กว่ามี error โผล่ไหม (มีแล้วใน starter)

```python
CASES = load_testdata()

@pytest.mark.parametrize("row", CASES, ids=[c["tc_id"] for c in CASES])
def test_register_from_excel(driver, base_url, row):
    driver.get(base_url + "/register")
    type_text(driver, "name", row["name"])
    type_text(driver, "email", row["email"])
    if row["agree"] == "Y":
        click(driver, "agree")
    click(driver, "register")

    if exists(driver, "error"):
        assert text_of(driver, "error") == row["expected_result"]
    else:
        assert row["expected_result"] in text_of(driver, "message")
```

- ช่องว่างใน Excel = `""` (starter แปลงให้แล้ว) จึงทดสอบ "ไม่กรอก" ได้ทันที
- ถ้าช่องเดียวต้องใส่หลายค่า ใช้ comma แล้ว `row["items"].split(",")` (ดู `examples/saucedemo`)
- อยากปิดบางแถว ให้ใส่ `N` ในคอลัมน์ `run`

---

## ขั้น E: แพตเทิร์นที่โจทย์ชอบให้ตรวจ

**เช็กการเรียงลำดับ**
```python
prices = [float(e.text.replace("$", "")) for e in driver.find_elements(*L["price"])]
assert prices == sorted(prices, reverse=True)      # มาก → น้อย
```

**เลือกตัวแรก / ตัวสุดท้ายของรายการ**
```python
items = driver.find_elements(*L["item"])
items[0].find_element(By.TAG_NAME, "button").click()    # ตัวแรก
items[-1].find_element(By.TAG_NAME, "button").click()   # ตัวสุดท้าย
```
XPath ก็ได้: `(//div[@class="item"])[1]` และ `(//div[@class="item"])[last()]`

**รวมราคา / คำนวณภาษี**
```python
total = round(sum(prices), 2)
assert total == round(item_total, 2)               # round ทั้งสองฝั่งเสมอ
assert abs(round(item_total * 0.08, 2) - tax) <= 0.01
```

**ดึงตัวเลขจากข้อความ**
```python
float("Item total: $39.98".split("$")[-1])         # 39.98
```

---

## เช็กลิสต์ก่อนส่ง
- [ ] ทุกเทสต์มี assert อย่างน้อย 1 อัน (ไม่มี assert = ไม่ได้ทดสอบอะไร)
- [ ] หลังทุกการเปลี่ยนหน้ามีการรอ (URL หรือ element)
- [ ] ตรวจครบทุกจุดที่โจทย์บอกว่า "ตรวจสอบ / Assert / เช็ก"
- [ ] เคสใน Excel ชีท TestCases ตรงกับแถวใน TestData (TC ID เดียวกัน)
- [ ] กรอก Actual Result + Status แล้ว
- [ ] รันรอบสุดท้ายผ่าน และปิด Excel ก่อนรัน
