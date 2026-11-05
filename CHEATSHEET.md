# Cheat Sheet: คำสั่งของแต่ละเครื่องมือ

## 1. ติดตั้งและรัน

| | ติดตั้ง | รัน |
| --- | --- | --- |
| Selenium | `py -m pip install selenium pytest` | `py -m pytest ไฟล์.py -v` |
| Playwright | `py -m pip install pytest-playwright` แล้ว `py -m playwright install chromium` | `py -m pytest ไฟล์.py --headed -v` |
| Robot | `py -m pip install robotframework robotframework-seleniumlibrary` | `py -m robot ไฟล์.robot` |
| อ่าน Excel (Python) | `py -m pip install openpyxl` | |
| อ่าน Excel (Robot) | `py -m pip install rpaframework` | `Library  RPA.Excel.Files` |
| YAML | `py -m pip install pyyaml` | Robot: `Variables  config.yaml` |
| Cypress | `npm init -y` แล้ว `npm install cypress --save-dev` | `npx cypress open` / `npx cypress run` |

**ตัวเลือกที่ใช้บ่อย**

| pytest | ความหมาย |
| --- | --- |
| `-v` | แสดงชื่อเทสต์ทีละตัว |
| `-k login` | รันเฉพาะเทสต์ที่ชื่อมีคำว่า login |
| `-x` | หยุดทันทีที่เจอเทสต์แรกที่ fail |
| `--html=report.html` | สร้างรายงาน (ต้องลง `pytest-html`) |
| `--headed` | (Playwright) เห็นเบราว์เซอร์ |
| `--slowmo 500` | (Playwright) ช้าลงทีละ 500 ms ดูทัน |

| robot | ความหมาย |
| --- | --- |
| `-t "ชื่อเทสต์"` | รันเฉพาะ test case นั้น |
| `-i tag` / `-e tag` | รันเฉพาะ tag / ยกเว้น tag |
| `-v NAME:value` | ส่งค่าตัวแปรตอนรัน |
| `-d results` | เก็บ log/report ไว้ในโฟลเดอร์ results |

## 2. คำสั่งในโค้ด

| ทำอะไร | Selenium | Playwright | Robot (SeleniumLibrary) | Cypress |
| --- | --- | --- | --- | --- |
| เปิดเว็บ | `driver.get(url)` | `page.goto(url)` | `Open Browser  url  chrome` / `Go To  url` | `cy.visit(url)` |
| หา 1 ตัว | `driver.find_element(By.ID, "x")` | `page.locator("#x")` | `id:x` | `cy.get('#x')` |
| หาหลายตัว | `driver.find_elements(...)` | `page.locator(".x").all()` | `Get WebElements  css:.x` | `cy.get('.x')` |
| พิมพ์ | `.send_keys("abc")` | `.fill("abc")` | `Input Text  loc  abc` | `.type('abc')` |
| ล้างช่อง | `.clear()` | `.fill("")` | `Clear Element Text  loc` | `.clear()` |
| คลิก | `.click()` | `.click()` | `Click Element  loc` | `.click()` |
| dropdown | `Select(el).select_by_visible_text("A")` | `.select_option(label="A")` | `Select From List By Label  loc  A` | `.select('A')` |
| checkbox | `.click()` | `.check()` | `Select Checkbox  loc` | `.check()` |
| อ่านข้อความ | `.text` | `.inner_text()` | `Get Text  loc` | `.invoke('text')` |
| อ่านค่าในช่อง | `.get_attribute("value")` | `.input_value()` | `Get Value  loc` | `.invoke('val')` |
| URL ปัจจุบัน | `driver.current_url` | `page.url` | `Get Location` | `cy.url()` |
| จับภาพ | `driver.save_screenshot("a.png")` | `page.screenshot(path="a.png")` | `Capture Page Screenshot` | `cy.screenshot()` |

## 3. การตรวจผล (Assert)

| ตรวจอะไร | Selenium (pytest) | Playwright | Robot |
| --- | --- | --- | --- |
| ข้อความเท่ากับ | `assert el.text == "A"` | `expect(loc).to_have_text("A")` | `Element Text Should Be  loc  A` |
| มีคำนี้ | `assert "A" in el.text` | `expect(loc).to_contain_text("A")` | `Element Should Contain  loc  A` |
| มองเห็น | `assert el.is_displayed()` | `expect(loc).to_be_visible()` | `Element Should Be Visible  loc` |
| URL | `assert "cart" in driver.current_url` | `expect(page).to_have_url(re.compile(".*cart"))` | `Location Should Contain  cart` |
| จำนวน | `assert len(els) == 2` | `expect(loc).to_have_count(2)` | `Page Should Contain Element  loc  limit=2` |
| ค่าในช่อง | `assert el.get_attribute("value") == "A"` | `expect(loc).to_have_value("A")` | `Textfield Value Should Be  loc  A` |
| ตัวเลข | `assert round(a, 2) == round(b, 2)` | เหมือน Selenium | `Should Be Equal As Numbers  a  b  precision=2` |
| เงื่อนไขทั่วไป | `assert a >= b` | `assert a >= b` | `Should Be True  ${a} >= ${b}` |

## 4. การรอ (กันเทสต์ flaky)

| | Selenium | Playwright | Robot |
| --- | --- | --- | --- |
| รอทั่วไป | `driver.implicitly_wait(5)` | รอให้เองทุก action | `Set Selenium Implicit Wait  5s` |
| รอ element โผล่ | `WebDriverWait(driver,10).until(EC.visibility_of_element_located(loc))` | `expect(loc).to_be_visible()` | `Wait Until Element Is Visible  loc` |
| รอคลิกได้ | `EC.element_to_be_clickable(loc)` | อัตโนมัติ | `Wait Until Element Is Enabled  loc` |
| รอ URL | `EC.url_contains("cart")` | `expect(page).to_have_url(...)` | `Wait Until Location Contains  cart` |
| รอข้อความ | `EC.text_to_be_present_in_element(loc, "A")` | `expect(loc).to_have_text("A")` | `Wait Until Element Contains  loc  A` |

**ห้ามใช้** `time.sleep()` / `Sleep` เป็นหลัก ใช้ได้แค่ตอน debug

## 5. ของที่เจอไม่บ่อยแต่ออกสอบได้

| เรื่อง | Selenium | Playwright | Robot |
| --- | --- | --- | --- |
| alert / confirm | `driver.switch_to.alert.accept()` | `page.on("dialog", lambda d: d.accept())` | `Handle Alert  ACCEPT` |
| iframe | `driver.switch_to.frame("id")` ... `switch_to.default_content()` | `page.frame_locator("#id").locator(...)` | `Select Frame  id:x` ... `Unselect Frame` |
| แท็บใหม่ | `driver.switch_to.window(driver.window_handles[-1])` | `with page.expect_popup() as p: ...` | `Switch Window  NEW` |
| hover | `ActionChains(driver).move_to_element(el).perform()` | `.hover()` | `Mouse Over  loc` |
| เลื่อนจอ | `driver.execute_script("arguments[0].scrollIntoView()", el)` | อัตโนมัติ | `Scroll Element Into View  loc` |
| กด Enter | `.send_keys(Keys.ENTER)` | `.press("Enter")` | `Press Keys  loc  ENTER` |

## 6. XPath ที่ใช้บ่อย

| ต้องการ | XPath |
| --- | --- |
| ปุ่มที่มีข้อความตรงตัว | `//button[text()="Login"]` |
| มีคำนี้อยู่ในข้อความ | `//h2[contains(text(),"Total")]` |
| ตาม attribute | `//input[@name="email"]` |
| ตัวแรก / ตัวสุดท้าย | `(//div[@class="item"])[1]` / `(//div[@class="item"])[last()]` |
| ลูกข้างใน | `(//div[@class="item"])[1]//button` |
| ช่องที่อยู่ถัดจาก label | `//label[text()="Email"]/following-sibling::input` |
| หลายเงื่อนไข | `//input[@type="text" and @name="q"]` |
