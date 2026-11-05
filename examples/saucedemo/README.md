# ตัวอย่าง: การบ้านทุกชิ้นบน saucedemo (รันผ่านแล้ว)

| การบ้าน | ไฟล์ |
| --- | --- |
| Selenium: สั่งซื้อ 1 ชิ้น | `python_tests/test_selenium_saucedemo.py` → `test_purchase_one_item` |
| Robot: Sort + 2 ชิ้น + Tax | `robot/tests/02_sort_multi_item_tax.robot` |
| Robot: E2E YAML + Excel (Scenario 1, 2) | `robot/tests/01_e2e_data_driven.robot` + `robot/config.yaml` + `testdata/testdata.xlsx` |
| Playwright: Sort + 2 ชิ้น + Tax | `python_tests/test_playwright_saucedemo.py` → `test_sort_multi_item_and_tax` |
| Cypress: Sort + 2 ชิ้น + Tax | `cypress_tests/cypress/e2e/sort_multi_item_tax.cy.js` |
| Data-driven จาก Excel (Selenium/Playwright) | `test_from_excel` ในทั้งสองไฟล์ |

## รัน (อยู่ในโฟลเดอร์นี้)
```
py -m pytest python_tests -v
```
```
cd robot
```
```
py -m robot tests
```
```
cd cypress_tests
```
```
npm install
```
```
npx cypress open
```

## Locator ของ saucedemo
ทุกอย่างมี `data-test` ใช้ `[data-test="..."]`:
`username`, `password`, `login-button`, `error`, `title`, `product-sort-container`, `inventory-item`,
`inventory-item-name`, `inventory-item-price`, `add-to-cart-<ชื่อสินค้า>`, `shopping-cart-link`,
`shopping-cart-badge`, `cart-list`, `checkout`, `firstName`, `lastName`, `postalCode`, `continue`,
`subtotal-label`, `tax-label`, `total-label`, `finish`, `complete-header`

ปุ่ม add-to-cart: ชื่อสินค้าตัวเล็ก แทนช่องว่างด้วย `-`
เช่น "Sauce Labs Bike Light" → `add-to-cart-sauce-labs-bike-light`

## Error message ของ saucedemo (ตรวจจาก source code ของเว็บ)
| กรณี | ข้อความ |
| --- | --- |
| user ถูกล็อก | `Epic sadface: Sorry, this user has been locked out.` |
| รหัสผิด | `Epic sadface: Username and password do not match any user in this service` |
| ไม่กรอก username | `Epic sadface: Username is required` |
| ไม่กรอก password | `Epic sadface: Password is required` |
| ไม่กรอก First / Last / Postal | `Error: First Name is required` / `Error: Last Name is required` / `Error: Postal Code is required` |
| สำเร็จ | `Thank you for your order!` |

## กับดักที่เจอจริงตอนทำชุดนี้
1. **Popup รหัสผ่านของ Chrome** บังปุ่ม → ปิดด้วย prefs ใน `conftest.py` / `keywords.robot` (ตามที่อาจารย์ให้)
2. **เว็บแสดง `Item total: $57.980000000000004`** → round 2 ตำแหน่งทั้งสองฝั่งก่อนเทียบ
3. **กดไอคอนตะกร้าแล้วนับสินค้าได้ 6** (ยังเป็นหน้าเดิม) → รอ URL `cart.html` ก่อนอ่านค่า
4. **Playwright `all_inner_texts()` ได้ list ว่าง** เพราะไม่รอ → `expect(...).to_have_count(n)` ก่อน
5. **ตะกร้าค้างจากเคสก่อน** → ล้าง cookie + `localStorage` ก่อนเริ่มแต่ละแถว (Robot ทำใน `Reset To Login Page`)
6. **Cypress** ยังไม่ได้รันจริง (เครื่องที่เตรียมชุดนี้โหลด Cypress ไม่ได้) ให้ลองรันเองที่บ้านก่อนสอบ
