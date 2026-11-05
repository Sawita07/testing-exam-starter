*** Settings ***
Documentation     HW: Sorting + เลือกสินค้าแพงสุด/ถูกสุด + ตรวจ Tax 8% + Finish
Resource          ../resources/keywords.robot
Suite Setup       Open Saucedemo
Suite Teardown    Close All Browsers
Test Teardown     Run Keyword If Test Failed    Capture Page Screenshot


*** Variables ***
${FIRST_ITEM}     (//*[@data-test="inventory-item"])[1]
${LAST_ITEM}      (//*[@data-test="inventory-item"])[last()]


*** Test Cases ***
Sort, Buy Most And Least Expensive, Verify Tax
    Reset To Login Page
    Login    ${default_user}[standard]    ${default_user}[password]
    Location Should Contain    /inventory.html

    # 1) Sorting Test
    Select From List By Label    css:[data-test="product-sort-container"]    Price (high to low)
    @{price_elements}=    Get WebElements    css:[data-test="inventory-item-price"]
    ${p1}=    Price To Number    ${{ $price_elements[0].text }}
    ${p2}=    Price To Number    ${{ $price_elements[1].text }}
    Should Be True    ${p1} >= ${p2}    msg=ราคาชิ้นแรก ${p1} ต้อง >= ชิ้นที่สอง ${p2}

    # 2) Multi-Item Selection (XPath: [1] = แพงสุด, [last()] = ถูกสุด)
    ${most}=     Get Text    xpath:${FIRST_ITEM}//*[@data-test="inventory-item-name"]
    ${least}=    Get Text    xpath:${LAST_ITEM}//*[@data-test="inventory-item-name"]
    Click Button    xpath:${FIRST_ITEM}//button
    Click Button    xpath:${LAST_ITEM}//button
    Element Text Should Be    css:[data-test="shopping-cart-badge"]    2

    # 3) Cart Navigation & Validation
    Click Element    css:[data-test="shopping-cart-link"]
    Wait Until Location Contains    cart.html    # รอให้เปลี่ยนหน้าก่อน ไม่งั้นจะนับสินค้าหน้าเดิม 6 ชิ้น
    Page Should Contain Element    css:[data-test="inventory-item"]    limit=2
    @{name_elements}=    Get WebElements    css:[data-test="inventory-item-name"]
    @{cart_names}=    Create List
    FOR    ${el}    IN    @{name_elements}
        Append To List    ${cart_names}    ${el.text}
    END
    List Should Contain Value    ${cart_names}    ${most}
    List Should Contain Value    ${cart_names}    ${least}

    # 4) Checkout & Calculation Verification
    Click Button    css:[data-test="checkout"]
    Fill Checkout Info    Somchai    Testing    10110
    Wait Until Location Contains    checkout-step-two
    @{overview_prices}=    Get WebElements    css:[data-test="inventory-item-price"]
    ${sum}=    Set Variable    ${0}
    FOR    ${el}    IN    @{overview_prices}
        ${p}=      Price To Number    ${el.text}
        ${sum}=    Evaluate    ${sum} + ${p}
    END
    ${item_total}=    Get Text    css:[data-test="subtotal-label"]
    ${item_total}=    Price To Number    ${item_total}
    ${tax}=           Get Text    css:[data-test="tax-label"]
    ${tax}=           Price To Number    ${tax}
    ${total}=         Get Text    css:[data-test="total-label"]
    ${total}=         Price To Number    ${total}

    # เว็บอาจแสดง 57.980000000000004 จึง round 2 ตำแหน่งก่อนเทียบ
    Should Be Equal As Numbers    ${sum}    ${item_total}    precision=2
    ${expected_tax}=    Evaluate    round(${item_total} * 0.08, 2)
    Should Be True    abs(${expected_tax} - ${tax}) <= 0.01    msg=Tax ผิด: คาด ${expected_tax} ได้ ${tax}
    ${calc_total}=    Evaluate    ${item_total} + ${tax}
    Should Be Equal As Numbers    ${calc_total}    ${total}    precision=2

    # 5) Complete & URL Verification
    Click Button    css:[data-test="finish"]
    Location Should Be    ${URL}/checkout-complete.html
    Element Text Should Be    css:[data-test="complete-header"]    Thank you for your order!
