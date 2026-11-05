"""
Playwright (Python) + pytest : ทดสอบ saucedemo
ติดตั้ง:  pip install pytest-playwright   แล้ว   playwright install
รัน:      pytest python_tests/test_playwright_saucedemo.py --headed
          (ไม่ใส่ --headed = รันแบบ headless)
"""
import re

import pytest
from playwright.sync_api import Page, expect

from conftest import load_testdata


def dt(name):
    return f'[data-test="{name}"]'


def money(text):
    return float(text.split("$")[-1])


def login(page: Page, base_url, username, password):
    page.goto(base_url + "/")
    page.fill(dt("username"), username)
    page.fill(dt("password"), password)
    page.click(dt("login-button"))


def fill_checkout(page: Page, first, last, postal):
    page.fill(dt("firstName"), first)
    page.fill(dt("lastName"), last)
    page.fill(dt("postalCode"), postal)
    page.click(dt("continue"))


# ---------- HW1: สั่งซื้อสินค้า 1 ชิ้นสำเร็จ ----------
def test_purchase_one_item(page: Page, base_url):
    login(page, base_url, "standard_user", "secret_sauce")
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))

    page.click(dt("add-to-cart-sauce-labs-backpack"))
    page.click(dt("shopping-cart-link"))
    page.click(dt("checkout"))
    fill_checkout(page, "Somchai", "Testing", "10110")

    expect(page.locator(dt("inventory-item-name"))).to_have_text(["Sauce Labs Backpack"])
    page.click(dt("finish"))
    expect(page.locator(dt("complete-header"))).to_have_text("Thank you for your order!")


# ---------- HW2: Sort + 2 สินค้า + คำนวณภาษี ----------
def test_sort_multi_item_and_tax(page: Page, base_url):
    login(page, base_url, "standard_user", "secret_sauce")
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))

    # 1) Sorting
    page.select_option(dt("product-sort-container"), label="Price (high to low)")
    expect(page.locator(dt("active-option"))).to_have_text("Price (high to low)")
    prices =[money(t) for t in page.locator(dt("inventory-item-price")).all_inner_texts()]
    assert prices[0] >= prices[1], f"เรียงราคาผิด: {prices}"

    # 2) แพงสุด = ตัวแรก, ถูกสุด = ตัวสุดท้าย
    items = page.locator(dt("inventory-item"))
    most, least = items.first, items.last
    most_name = most.locator(dt("inventory-item-name")).inner_text()
    least_name = least.locator(dt("inventory-item-name")).inner_text()
    most.locator("button").click()
    least.locator("button").click()
    expect(page.locator(dt("shopping-cart-badge"))).to_have_text("2")

    # 3) Cart
    page.click(dt("shopping-cart-link"))
    expect(page).to_have_url(re.compile(r".*/cart\.html"))
    cart = page.locator(dt("inventory-item-name"))
    expect(cart).to_have_count(2)
    assert set(cart.all_inner_texts()) == {most_name, least_name}

    # 4) Checkout + คำนวณ
    page.click(dt("checkout"))
    fill_checkout(page, "Somchai", "Testing", "10110")

    # all_inner_texts() ไม่รอ element เอง ต้อง expect ให้หน้า Overview โหลดก่อน
    expect(page).to_have_url(re.compile(r".*/checkout-step-two\.html"))
    expect(page.locator(dt("inventory-item-price"))).to_have_count(2)
    item_prices =[money(t) for t in page.locator(dt("inventory-item-price")).all_inner_texts()]
    item_total = money(page.inner_text(dt("subtotal-label")))
    tax = money(page.inner_text(dt("tax-label")))
    total = money(page.inner_text(dt("total-label")))

    assert round(sum(item_prices), 2) == round(item_total, 2)
    assert abs(round(item_total * 0.08, 2) - tax) <= 0.01
    assert round(item_total + tax, 2) == round(total, 2)

    # 5) Finish
    page.click(dt("finish"))
    expect(page).to_have_url(base_url + "/checkout-complete.html")
    expect(page.locator(dt("complete-header"))).to_have_text("Thank you for your order!")


# ---------- Data-driven จาก Excel ----------
CASES = load_testdata()


@pytest.mark.parametrize("row", CASES, ids=[c["tc_id"] for c in CASES])
def test_from_excel(page: Page, base_url, row):
    login(page, base_url, row["username"], row["password"])
    error = page.locator(dt("error"))
    if error.count() > 0:                       # negative: login ไม่ผ่าน
        expect(error).to_have_text(row["expected_result"])
        return

    for name in [x.strip() for x in row["items_to_add"].split(",") if x.strip()]:
        page.click(dt("add-to-cart-" + name.lower().replace(" ", "-")))

    page.click(dt("shopping-cart-link"))
    page.click(dt("checkout"))
    fill_checkout(page, row["first_name"], row["last_name"], row["postal_code"])

    if error.count() > 0:                       # negative: กรอกไม่ครบ
        expect(error).to_have_text(row["expected_result"])
        return

    page.click(dt("finish"))
    expect(page.locator(dt("complete-header"))).to_have_text(row["expected_result"])
