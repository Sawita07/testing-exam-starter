// HW: Sorting + เลือกสินค้าแพงสุด/ถูกสุด + ตรวจ Tax 8% + Finish
const dt = (name) => `[data-test="${name}"]`;
const money = (text) => parseFloat(text.split('$').pop());

describe('Saucedemo - Sort, Multi-item, Tax', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.get(dt('username')).type('standard_user');
    cy.get(dt('password')).type('secret_sauce');
    cy.get(dt('login-button')).click();
    cy.url().should('include', '/inventory.html');
  });

  it('sorts high to low, buys most & least expensive, verifies totals', () => {
    // 1) Sorting
    cy.get(dt('product-sort-container')).select('Price (high to low)');
    cy.get(dt('inventory-item-price')).then(($prices) => {
      const prices = [...$prices].map((el) => money(el.innerText));
      expect(prices[0]).to.be.at.least(prices[1]);
    });

    // 2) แพงสุด = ตัวแรก, ถูกสุด = ตัวสุดท้าย  (.as() เก็บค่าไว้ใช้ทีหลัง)
    cy.get(dt('inventory-item')).first().find(dt('inventory-item-name')).invoke('text').as('most');
    cy.get(dt('inventory-item')).last().find(dt('inventory-item-name')).invoke('text').as('least');
    cy.get(dt('inventory-item')).first().find('button').click();
    cy.get(dt('inventory-item')).last().find('button').click();
    cy.get(dt('shopping-cart-badge')).should('have.text', '2');

    // 3) Cart มี 2 ชิ้นตามที่เลือก
    cy.get(dt('shopping-cart-link')).click();
    cy.get(dt('inventory-item')).should('have.length', 2);
    cy.get('@most').then((most) => cy.get(dt('cart-list')).should('contain', most));
    cy.get('@least').then((least) => cy.get(dt('cart-list')).should('contain', least));

    // 4) Checkout + คำนวณ
    cy.get(dt('checkout')).click();
    cy.get(dt('firstName')).type('Somchai');
    cy.get(dt('lastName')).type('Testing');
    cy.get(dt('postalCode')).type('10110');
    cy.get(dt('continue')).click();

    cy.get(dt('inventory-item-price')).should('have.length', 2).then(($prices) => {
      const sum = [...$prices].reduce((acc, el) => acc + money(el.innerText), 0);
      cy.get(dt('subtotal-label')).invoke('text').then((itemText) => {
        const itemTotal = money(itemText);
        expect(sum.toFixed(2)).to.eq(itemTotal.toFixed(2)); // round ทั้งสองฝั่ง
        cy.get(dt('tax-label')).invoke('text').then((taxText) => {
          const tax = money(taxText);
          expect(Math.abs(itemTotal * 0.08 - tax)).to.be.at.most(0.01);
          cy.get(dt('total-label')).invoke('text').then((totalText) => {
            expect((itemTotal + tax).toFixed(2)).to.eq(money(totalText).toFixed(2));
          });
        });
      });
    });

    // 5) Finish
    cy.get(dt('finish')).click();
    cy.url().should('eq', Cypress.config('baseUrl') + '/checkout-complete.html');
    cy.get(dt('complete-header')).should('have.text', 'Thank you for your order!');
  });
});
