"""
Playwright starter : ก๊อปไฟล์นี้ไปใช้ตอนสอบ แล้วแก้ 2 ที่
  (1) กล่อง L ด้านบน          -> ใส่ selector ของเว็บข้อสอบ
  (2) ฟังก์ชัน test_ ด้านล่าง  -> เรียงขั้นตอนตามโจทย์
รัน:  py -m pytest test_playwright_starter.py --headed -v
"""
import re

import pytest
from playwright.sync_api import Page, expect

from conftest import load_testdata

# ===== (1) LOCATORS: Playwright ใช้ string ได้ทั้ง CSS และ XPath =====
L = {
    "username":     '[data-test="username"]',
    "password":     '[data-test="password"]',
    "login_button": '[data-test="login-button"]',
    "error":        '[data-test="error"]',
    "page_title":   '[data-test="title"]',
    # "search":   "#search-box",
    # "submit":   'xpath=//button[text()="Submit"]',
    # "menu":     'text=Menu',
}
# ====================================================================


# ---------- (2) TEST แบบตายตัว 1 เคส ----------
def test_login_success(page: Page, base_url):
    page.goto(base_url + "/")
    page.fill(L["username"], "standard_user")
    page.fill(L["password"], "secret_sauce")
    page.click(L["login_button"])

    expect(page).to_have_url(re.compile(r".*inventory"))      # รอเปลี่ยนหน้าก่อนเสมอ
    expect(page.locator(L["page_title"])).to_have_text("Products")


# ---------- (2) TEST แบบอ่านข้อมูลจาก Excel ----------
CASES = load_testdata()

@pytest.mark.parametrize("row", CASES, ids=[c["tc_id"] for c in CASES])
def test_login_from_excel(page: Page, base_url, row):
    page.goto(base_url + "/")
    page.fill(L["username"], row["username"])
    page.fill(L["password"], row["password"])
    page.click(L["login_button"])

    error = page.locator(L["error"])
    if error.count() > 0:                                       # negative case
        expect(error).to_have_text(row["expected_result"])
    else:                                                       # positive case
        expect(page.locator(L["page_title"])).to_have_text(row["expected_result"])
