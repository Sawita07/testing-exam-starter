"""
Selenium starter : ก๊อปไฟล์นี้ไปใช้ตอนสอบ แล้วแก้ 2 ที่
  (1) กล่อง LOCATORS ด้านบน  -> ใส่ selector ของเว็บข้อสอบ
  (2) ฟังก์ชัน test_ ด้านล่าง -> เรียงขั้นตอนตามโจทย์
รัน:  py -m pytest test_selenium_starter.py -v
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from conftest import load_testdata

# ===== (1) LOCATORS: จดจาก F12 ของเว็บข้อสอบ =====
# รูปแบบ  ชื่อที่เราตั้งเอง: (วิธีหา, ค่า)
L = {
    "username":     (By.CSS_SELECTOR, '[data-test="username"]'),
    "password":     (By.CSS_SELECTOR, '[data-test="password"]'),
    "login_button": (By.CSS_SELECTOR, '[data-test="login-button"]'),
    "error":        (By.CSS_SELECTOR, '[data-test="error"]'),
    "page_title":   (By.CSS_SELECTOR, '[data-test="title"]'),
    # ตัวอย่างแบบอื่น:
    # "search":  (By.ID, "search-box"),
    # "submit":  (By.XPATH, '//button[text()="Submit"]'),
    # "menu":    (By.XPATH, '//a[contains(text(),"Menu")]'),
}
# ================================================


# ---------- ตัวช่วย (ใช้ได้ทุกเว็บ ไม่ต้องแก้) ----------
def find(driver, key):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located(L[key]))

def click(driver, key):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(L[key])).click()

def type_text(driver, key, text):
    el = find(driver, key)
    el.clear()
    el.send_keys(text)

def text_of(driver, key):
    return find(driver, key).text

def select_by_text(driver, key, visible_text):
    Select(find(driver, key)).select_by_visible_text(visible_text)

def exists(driver, key):
    return len(driver.find_elements(*L[key])) > 0

def wait_url(driver, part):
    WebDriverWait(driver, 10).until(EC.url_contains(part))


# ---------- (2) TEST แบบตายตัว 1 เคส (ทำให้ผ่านก่อน) ----------
def test_login_success(driver, base_url):
    driver.get(base_url + "/")
    type_text(driver, "username", "standard_user")
    type_text(driver, "password", "secret_sauce")
    click(driver, "login_button")

    wait_url(driver, "inventory")
    assert text_of(driver, "page_title") == "Products"


# ---------- (2) TEST แบบอ่านข้อมูลจาก Excel ----------
CASES = load_testdata()

@pytest.mark.parametrize("row", CASES, ids=[c["tc_id"] for c in CASES])
def test_login_from_excel(driver, base_url, row):
    driver.get(base_url + "/")
    type_text(driver, "username", row["username"])
    type_text(driver, "password", row["password"])
    click(driver, "login_button")

    if exists(driver, "error"):                     # negative case
        assert text_of(driver, "error") == row["expected_result"]
    else:                                           # positive case
        assert text_of(driver, "page_title") == row["expected_result"]
