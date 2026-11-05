*** Settings ***
Documentation     Robot Framework starter : ก๊อปไปใช้ตอนสอบ แก้ Variables (locator) กับ Test Cases
...               รัน:  py -m robot starter.robot
Library           SeleniumLibrary
Library           OperatingSystem
Library           RPA.Excel.Files
Variables         config.yaml
Suite Setup       Open Website
Suite Teardown    Close All Browsers
Test Teardown     Run Keyword If Test Failed    Capture Page Screenshot


*** Variables ***
# ===== LOCATORS: จดจาก F12 ของเว็บข้อสอบ =====
${USERNAME_INPUT}    css:[data-test="username"]
${PASSWORD_INPUT}    css:[data-test="password"]
${LOGIN_BUTTON}      css:[data-test="login-button"]
${ERROR_MSG}         css:[data-test="error"]
${PAGE_TITLE}        css:[data-test="title"]
# แบบอื่น:  id:search-box   name:email   xpath://button[text()="Submit"]
# ============================================


*** Test Cases ***
Login Success (ข้อมูลตายตัว)
    Go To    ${URL}
    Login    ${default_user}[username]    ${default_user}[password]
    Wait Until Location Contains    inventory
    Element Text Should Be    ${PAGE_TITLE}    Products

Login From Excel (Data-Driven)
    ${rows}=    Read Excel Rows
    FOR    ${row}    IN    @{rows}
        Continue For Loop If    '${row}[run]' != 'Y'
        Run Keyword And Continue On Failure    Check Login Row    ${row}
    END


*** Keywords ***
Open Website
    ${URL}=    Get Variable Value    ${BASE_URL}    ${env}[url]
    Set Suite Variable    ${URL}
    ${headless}=    Get Variable Value    ${HEADLESS}    ${env}[headless]
    ${prefs}=    Set Variable    add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False, "profile.password_manager_leak_detection": False})
    IF    ${headless}
        Open Browser    ${URL}    headlesschrome    options=${prefs};add_argument("--no-sandbox")
    ELSE
        Open Browser    ${URL}    chrome    options=${prefs}
        Maximize Browser Window
    END
    Set Selenium Implicit Wait    ${env}[implicit_wait]

Login
    [Arguments]    ${username}    ${password}
    Input Text        ${USERNAME_INPUT}    ${username}
    Input Password    ${PASSWORD_INPUT}    ${password}
    Click Button      ${LOGIN_BUTTON}

Read Excel Rows
    [Documentation]    อ่านชีท TestData (แถวแรก = หัวคอลัมน์) ช่องว่างแปลงเป็น ""
    ${file}=    Normalize Path    ${CURDIR}/${env}[excel_file]
    Open Workbook    ${file}
    ${rows}=    Read Worksheet    name=TestData    header=True
    Close Workbook
    ${clean}=    Evaluate    [{k: ('' if v is None else str(v).strip()) for k, v in r.items()} for r in $rows if r.get('tc_id')]
    RETURN    ${clean}

Check Login Row
    [Arguments]    ${row}
    Log To Console    \n>> ${row}[tc_id] ${row}[testcase_name]
    Go To    ${URL}
    Delete All Cookies
    Go To    ${URL}
    Login    ${row}[username]    ${row}[password]
    ${has_error}=    Run Keyword And Return Status    Page Should Contain Element    ${ERROR_MSG}
    IF    ${has_error}
        Element Text Should Be    ${ERROR_MSG}     ${row}[expected_result]
    ELSE
        Element Text Should Be    ${PAGE_TITLE}    ${row}[expected_result]
    END
