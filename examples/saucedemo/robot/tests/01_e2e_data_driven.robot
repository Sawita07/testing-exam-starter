*** Settings ***
Documentation     HW: E2E Test Suite (YAML + Excel) - Scenario 1 positive, Scenario 2 negative
Resource          ../resources/keywords.robot
Suite Setup       Open Saucedemo
Suite Teardown    Close All Browsers
Test Teardown     Run Keyword If Test Failed    Capture Page Screenshot


*** Test Cases ***
Scenario 1: End-to-End Successful Purchase (Data-Driven)
    [Tags]    positive
    ${rows}=    Read Test Data From Excel
    FOR    ${row}    IN    @{rows}
        ${run}=         Cell    ${row}    run
        ${expected}=    Cell    ${row}    expected_result
        Continue For Loop If    '${run}' != 'Y'
        Continue For Loop If    not '${expected}'.startswith('Thank you')
        Run Keyword And Continue On Failure    Run Purchase Scenario    ${row}
    END

Scenario 2: Negative Case - Error Validation
    [Tags]    negative
    ${rows}=    Read Test Data From Excel
    FOR    ${row}    IN    @{rows}
        ${run}=         Cell    ${row}    run
        ${expected}=    Cell    ${row}    expected_result
        Continue For Loop If    '${run}' != 'Y'
        Continue For Loop If    '${expected}'.startswith('Thank you')
        Run Keyword And Continue On Failure    Run Purchase Scenario    ${row}
    END
