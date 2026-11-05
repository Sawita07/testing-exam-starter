*** Settings ***
Documentation     Keyword กลางที่ทุก test suite ใช้ร่วมกัน
Library           SeleniumLibrary
Library           String
Library           Collections
Library           OperatingSystem
Library           RPA.Excel.Files
Variables         ../config.yaml


*** Keywords ***
# ---------------- Browser ----------------
Open Saucedemo
    [Documentation]    เปิดเบราว์เซอร์ตาม config.yaml
    ...                override ได้ตอนรัน เช่น robot -v BASE_URL:http://localhost:3000 -v HEADLESS:True tests
    ${url}=    Get Variable Value    ${BASE_URL}    ${env}[url]
    Set Suite Variable    ${URL}    ${url}
    ${prefs}=    Set Variable
    ...    add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False, "profile.password_manager_leak_detection": False})
    ${headless}=    Get Variable Value    ${HEADLESS}    ${env}[headless]
    IF    ${headless}
        Open Browser    ${URL}    headlesschrome    options=${prefs};add_argument("--no-sandbox");add_argument("--window-size=1280,900")
    ELSE
        Open Browser    ${URL}    ${env}[browser]    options=${prefs}
        Maximize Browser Window
    END
    Set Selenium Implicit Wait    ${timeout}[implicit_wait]
    Set Selenium Timeout    ${timeout}[explicit_wait]

Reset To Login Page
    [Documentation]    ล้าง session และตะกร้า เพื่อให้แต่ละแถวข้อมูลเริ่มใหม่ (tests ต้อง independent)
    Go To    ${URL}
    Delete All Cookies
    Execute Javascript    window.localStorage.clear();
    Go To    ${URL}
    Wait Until Element Is Visible    css:[data-test="login-button"]

# ---------------- Actions ----------------
Login
    [Arguments]    ${username}    ${password}
    Input Text        css:[data-test="username"]    ${username}
    Input Password    css:[data-test="password"]    ${password}
    Click Button      css:[data-test="login-button"]

Add Items To Cart
    [Documentation]    รับชื่อสินค้าคั่นด้วย comma เช่น "Sauce Labs Backpack, Sauce Labs Bike Light"
    [Arguments]    ${items_text}
    @{items}=    Split String    ${items_text}    ,
    FOR    ${item}    IN    @{items}
        ${item}=    Strip String    ${item}
        Continue For Loop If    '${item}' == ''
        ${slug}=    Convert To Lower Case    ${item}
        ${slug}=    Replace String    ${slug}    ${SPACE}    -
        Click Button    css:[data-test="add-to-cart-${slug}"]
    END

Go To Checkout
    Click Element    css:[data-test="shopping-cart-link"]
    Click Button     css:[data-test="checkout"]

Fill Checkout Info
    [Arguments]    ${first}    ${last}    ${postal}
    Input Text    css:[data-test="firstName"]     ${first}
    Input Text    css:[data-test="lastName"]      ${last}
    Input Text    css:[data-test="postalCode"]    ${postal}
    Click Button    css:[data-test="continue"]

Error Is Shown
    ${count}=    Get Element Count    css:[data-test="error"]
    RETURN    ${{ ${count} > 0 }}

Price To Number
    [Documentation]    "Item total: $39.98" -> 39.98
    [Arguments]    ${text}
    ${num}=    Evaluate    float($text.split('$')[-1])
    RETURN    ${num}

# ---------------- Excel ----------------
Read Test Data From Excel
    [Documentation]    อ่านชีท TestData เป็น list ของ dictionary (แถวแรก = header)
    ${file}=    Normalize Path    ${CURDIR}/${excel}[file]
    Open Workbook    ${file}
    ${rows}=    Read Worksheet    name=${excel}[sheet]    header=True
    Close Workbook
    RETURN    ${rows}

Cell
    [Documentation]    ดึงค่าจาก row ถ้าช่องว่าง (None) ให้เป็น ""
    [Arguments]    ${row}    ${key}
    ${value}=    Evaluate    '' if $row.get($key) is None else str($row.get($key)).strip()
    RETURN    ${value}

# ---------------- Flow หลักต่อ 1 แถวข้อมูล ----------------
Run Purchase Scenario
    [Documentation]    ทำตาม flow ทั้งหมด แล้วเทียบผลกับ expected_result ใน Excel
    [Arguments]    ${row}
    ${tc}=          Cell    ${row}    tc_id
    ${user}=        Cell    ${row}    username
    ${pass}=        Cell    ${row}    password
    ${items}=       Cell    ${row}    items_to_add
    ${first}=       Cell    ${row}    first_name
    ${last}=        Cell    ${row}    last_name
    ${postal}=      Cell    ${row}    postal_code
    ${expected}=    Cell    ${row}    expected_result
    Log To Console    \n>> ${tc}: ${expected}

    Reset To Login Page
    Login    ${user}    ${pass}
    ${has_error}=    Error Is Shown
    IF    ${has_error}
        Element Text Should Be    css:[data-test="error"]    ${expected}
        RETURN
    END

    Add Items To Cart    ${items}
    Go To Checkout
    Fill Checkout Info    ${first}    ${last}    ${postal}
    ${has_error}=    Error Is Shown
    IF    ${has_error}
        Element Text Should Be    css:[data-test="error"]    ${expected}
        RETURN
    END

    Click Button    css:[data-test="finish"]
    Element Text Should Be    css:[data-test="complete-header"]    ${expected}
