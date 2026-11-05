"""
conftest.py = ไฟล์กลางของ pytest
fixture ในไฟล์นี้ใช้ได้ทุกไฟล์ test_*.py ในโฟลเดอร์เดียวกันโดยไม่ต้อง import
"""
import os
from pathlib import Path

import pytest
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ตั้งค่า URL ได้ผ่าน environment variable เช่น  BASE_URL=http://localhost:3000 pytest
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com").rstrip("/")
TESTDATA_FILE = Path(__file__).resolve().parent.parent / "testdata" / "testdata.xlsx"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def driver():
    """Selenium driver: setup ก่อน yield, teardown หลัง yield"""
    chrome_options = Options()
    # ปิด popup "Change your password" / password manager ของ Chrome (ตามที่อาจารย์ให้ไว้)
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    if os.getenv("HEADLESS") == "1":
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")              # จำเป็นเวลารันใน Docker/CI
        chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,900")

    drv = webdriver.Chrome(options=chrome_options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


def load_testdata(sheet="TestData"):
    """อ่าน Excel เป็น list ของ dict  (แถวแรก = ชื่อคอลัมน์) ข้ามแถวที่ run != Y"""
    wb = load_workbook(TESTDATA_FILE, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    header = [str(h).strip() for h in rows[0]]
    data = []
    for row in rows[1:]:
        if row[0] is None:
            continue
        item = {h: ("" if v is None else str(v).strip()) for h, v in zip(header, row)}
        if item.get("run", "Y").upper() == "Y":
            data.append(item)
    wb.close()
    return data
