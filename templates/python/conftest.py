"""
conftest.py : ไฟล์กลางของ pytest (ไม่ต้องแก้ ยกเว้นชื่อไฟล์/ชีท Excel)
- fixture `driver`  = เปิด/ปิด Chrome ให้เทสต์ Selenium
- fixture `base_url` = URL เว็บที่ทดสอบ
- load_testdata()   = อ่าน Excel เป็น list ของ dict
"""
import os
from pathlib import Path

import pytest
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ===== แก้ตรงนี้ถ้าจำเป็น =====
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com").rstrip("/")
EXCEL_FILE = Path(__file__).resolve().parent.parent / "testdata" / "testdata.xlsx"
EXCEL_SHEET = "TestData"
# =============================


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def driver():
    options = Options()
    # ปิด popup password manager ของ Chrome (ตัวที่ชอบเด้งมาบังปุ่ม)
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1280,900")

    drv = webdriver.Chrome(options=options)   # setup
    drv.implicitly_wait(5)
    yield drv                                  # ส่ง driver ให้เทสต์ใช้
    drv.quit()                                 # teardown


def load_testdata(sheet=EXCEL_SHEET):
    """แถวแรกของชีท = ชื่อคอลัมน์ / ข้ามแถวที่คอลัมน์ run ไม่ใช่ Y / ช่องว่างกลายเป็น "" """
    wb = load_workbook(EXCEL_FILE, data_only=True)
    rows = list(wb[sheet].iter_rows(values_only=True))
    wb.close()
    header = [str(h).strip() for h in rows[0]]
    data = []
    for row in rows[1:]:
        if row[0] is None:
            continue
        item = {h: ("" if v is None else str(v).strip()) for h, v in zip(header, row)}
        if item.get("run", "Y").upper() == "Y":
            data.append(item)
    return data
