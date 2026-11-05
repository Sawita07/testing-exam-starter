const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    // เปลี่ยนได้ตอนรัน: npx cypress run --config baseUrl=http://localhost:3000
    baseUrl: 'https://www.saucedemo.com',
    specPattern: 'cypress/e2e/**/*.cy.js',
    supportFile: false,
    viewportWidth: 1280,
    viewportHeight: 900,
    defaultCommandTimeout: 10000,
    screenshotOnRunFailure: true,
  },
});
