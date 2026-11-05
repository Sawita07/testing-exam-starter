"""
Selenium + pytest : ทดสอบ saucedemo
รัน:  pytest python_tests/test_selenium_saucedemo.py -v
รันพร้อมรายงาน HTML:  pytest python_tests/test_selenium_saucedemo.py --html=report.html
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from conftest import load_testdata


# ---------- helper (ใช้ซ้ำหลายเทสต์) ----------
def css(driver, selector):
    return driver.find_element(By.CSS_SELECTOR, selector)


def dt(name):
    """สร้าง CSS selector จาก data-test เช่น dt('username') -> [data-test="username"]"""
    return f'[data-test="{name}"]'


def money(text):
    """แปลง 'Item total: $39.98' หรือ '$29.99' -> 39.98"""
    return float(text.split("$")[-1])


def login(driver, base_url, username, password):
    driver.get(base_url + "/")
    css(driver, dt("username")).send_keys(username)
    css(driver, dt("password")).send_keys(password)
    css(driver, dt("login-button")).click()


def fill_checkout(driver, first, last, postal):
    css(driver, dt("firstName")).send_keys(first)
    css(driver, dt("lastName")).send_keys(last)
    css(driver, dt("postalCode")).send_keys(postal)
    css(driver, dt("continue")).click()


# ---------- HW1: สั่งซื้อสินค้า 1 ชิ้นสำเร็จ ----------
def test_purchase_one_item(driver, base_url):
    wait = WebDriverWait(driver, 10)
    login(driver, base_url, "standard_user", "secret_sauce")

    wait.until(EC.url_contains("/inventory.html"))
    assert "/inventory.html" in driver.current_url

    css(driver, dt("add-to-cart-sauce-labs-backpack")).click()
    css(driver, dt("shopping-cart-link")).click()
    css(driver, dt("checkout")).click()

    fill_checkout(driver, "Somchai", "Testing", "10110")
    wait.until(EC.url_contains("checkout-step-two"))

    names =[e.text for e in driver.find_elements(By.CSS_SELECTOR, dt("inventory-item-name"))]
    assert names == ["Sauce Labs Backpack"]

    css(driver, dt("finish")).click()
    header = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, dt("complete-header"))))
    assert header.text == "Thank you for your order!"


# ---------- HW2: Sort + 2 สินค้า + คำนวณภาษี ----------
def test_sort_multi_item_and_tax(driver, base_url):
    wait = WebDriverWait(driver, 10)
    login(driver, base_url, "standard_user", "secret_sauce")
    wait.until(EC.url_contains("/inventory.html"))

    # 1) Sorting: Price (high to low)
    Select(css(driver, dt("product-sort-container"))).select_by_visible_text("Price (high to low)")
    prices = [money(e.text) for e in driver.find_elements(By.CSS_SELECTOR, dt("inventory-item-price"))]
    assert prices[0] >= prices[1], f"เรียงราคาผิด: {prices}"
    assert prices == sorted(prices, reverse=True)  # ตรวจทั้งหน้า (เกินโจทย์ แต่ดี)

    # 2) เลือกแพงสุด (ตัวแรก) และถูกสุด (ตัวสุดท้าย)
    items = driver.find_elements(By.CSS_SELECTOR, dt("inventory-item"))
    most = items[0].find_element(By.CSS_SELECTOR, dt("inventory-item-name")).text
    least = items[-1].find_element(By.CSS_SELECTOR, dt("inventory-item-name")).text
    items[0].find_element(By.TAG_NAME, "button").click()
    items[-1].find_element(By.TAG_NAME, "button").click()
    assert css(driver, dt("shopping-cart-badge")).text == "2"

    # 3) Cart มี 2 ชิ้นตามที่เลือก
    css(driver, dt("shopping-cart-link")).click()
    wait.until(EC.url_contains("cart.html"))  # รอเปลี่ยนหน้าก่อนอ่านค่า
    cart_names =[e.text for e in driver.find_elements(By.CSS_SELECTOR, dt("inventory-item-name"))]
    assert len(cart_names) == 2
    assert set(cart_names) == {most, least}

    # 4) Checkout + ตรวจการคำนวณ
    css(driver, dt("checkout")).click()
    fill_checkout(driver, "Somchai", "Testing", "10110")
    wait.until(EC.url_contains("checkout-step-two"))

    item_prices =[money(e.text) for e in driver.find_elements(By.CSS_SELECTOR, dt("inventory-item-price"))]
    item_total = money(css(driver, dt("subtotal-label")).text)
    tax = money(css(driver, dt("tax-label")).text)
    total = money(css(driver, dt("total-label")).text)

    # ระวัง! เว็บอาจแสดง "Item total: $57.980000000000004" (ทศนิยม float)
    # จึงต้อง round ทั้งสองฝั่งเป็น 2 ตำแหน่งก่อนเทียบเสมอ
    assert round(sum(item_prices), 2) == round(item_total, 2)
    assert abs(round(item_total * 0.08, 2) - tax) <= 0.01               # Tax 8%
    assert round(item_total + tax, 2) == round(total, 2)                # Item Total + Tax = Total

    # 5) Finish + URL + ข้อความ
    css(driver, dt("finish")).click()
    wait.until(EC.url_contains("checkout-complete"))
    assert driver.current_url == base_url + "/checkout-complete.html"
    assert css(driver, dt("complete-header")).text == "Thank you for your order!"


# ---------- Data-driven จาก Excel (ทั้ง positive และ negative) ----------
CASES = load_testdata()


@pytest.mark.parametrize("row", CASES, ids=[c["tc_id"] for c in CASES])
def test_from_excel(driver, base_url, row):
    login(driver, base_url, row["username"], row["password"])

    # Negative: login ไม่ผ่าน
    errors = driver.find_elements(By.CSS_SELECTOR, dt("error"))
    if errors:
        assert errors[0].text == row["expected_result"]
        return

    for name in [x.strip() for x in row["items_to_add"].split(",") if x.strip()]:
        slug = name.lower().replace(" ", "-")
        css(driver, dt(f"add-to-cart-{slug}")).click()

    css(driver, dt("shopping-cart-link")).click()
    css(driver, dt("checkout")).click()
    fill_checkout(driver, row["first_name"], row["last_name"], row["postal_code"])

    # Negative: กรอกข้อมูลไม่ครบ
    errors = driver.find_elements(By.CSS_SELECTOR, dt("error"))
    if errors:
        assert errors[0].text == row["expected_result"]
        return

    css(driver, dt("finish")).click()
    assert css(driver, dt("complete-header")).text == row["expected_result"]
