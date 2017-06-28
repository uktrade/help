var settings = require('../settings/settings'),
    triage = require('../settings/triage'),
    form = require('../settings/form');


describe('triage page', function() {

    beforeEach(function () {
        browser.ignoreSynchronization = true;
    });

    it('Should be on the triage page', function() {
        browser.get(settings.navigate.triage);
        expect(settings.pageHeader.getText()).toEqual('ebay');
    });

    describe('Benefits of applying section', function() {

        it('Should be expanded with document is loaded', function () {
            expect(triage.benefitsSection.isDisplayed()).toBe(true);
        });

        it('Should be hidden', function () {
            triage.benefitsSectionButton.click();
            expect(triage.benefitsSection.isDisplayed()).toBe(false);
        });

        it('Should be expanded', function () {
            triage.benefitsSectionButton.click();
            expect(triage.benefitsSection.isDisplayed()).toBe(true);
        });
    });

    describe('Your business section', function () {

        it('Should be on the business section', function () {
            expect(triage.sectionHeaders.get(0).isDisplayed()).toBe(true);
        });

        it('should display all error messages', function () {
            triage.formNextButton.get(0).click();
            expect(form.errorMessages.get(0).getText()).toEqual(triage.companyNameErrorMessage);
            expect(form.errorMessages.get(4).getText()).toEqual(triage.companyWebsiteErrorMessage);
        });

        describe('Company House search', function () {

            it('Should lookup for company', function () {
                triage.companyNameInputField.sendKeys('apple');
                triage.companySearchButton.click();
                triage.companyList.get(0).click();
                triage.companyWebsiteInputField.sendKeys(settings.user.website);
                expect(form.errorMessages.get(0).getText()).toEqual('');
                expect(triage.companyNumberInputField.getAttribute('value')).not.toBe('');
                expect(triage.companyPostCodeInputField.getAttribute('value')).not.toBe('');
            });

        });
    });

    describe('Business details section', function () {

        it('Should be on the details section', function () {
            triage.formNextButton.get(0).click();
            expect(triage.sectionHeaders.get(1).isDisplayed()).toBe(true);
        });

        it('should display all error messages', function () {
            triage.formNextButton.get(1).click();
            expect(form.errorMessages.get(5).getText()).toEqual(triage.companyTurnoverErrorMessage);
            expect(form.errorMessages.get(6).getText()).toEqual(triage.companySkuErrorMessage);
            expect(form.errorMessages.get(7).getText()).toEqual(triage.companyTradeMarkErrorMessage);
        });
    });

    describe('Your experience section', function () {

        it('Should be on the details section', function () {
            triage.turnoverInputField.click();
            triage.skuInputField.sendKeys('123');
            triage.trademarkInputField.click();
            triage.formNextButton.get(1).click();
            expect(triage.sectionHeaders.get(2).isDisplayed()).toBe(true);
        });

        it('should display all error messages', function () {
            triage.formNextButton.get(2).click();
            expect(form.errorMessages.get(8).getText()).toEqual(triage.soldProductErrorMessage);
            expect(form.errorMessages.get(9).getText()).toEqual(triage.descriptionErrorMessage);
        });

    });

    describe('Contact details section', function () {

        it('should be on the contact details section', function () {
            triage.soldOutsideInputField.click();
            triage.descriptionInputField.sendKeys(settings.user.businessPitch);
            browser.sleep(1000)
            triage.formNextButton.get(2).click();
            expect(triage.sectionHeaders.get(3).isDisplayed()).toBe(true);
        });

        it('should display all error messages', function () {
            triage.formNextButton.get(3).click();
            expect(form.errorMessages.get(10).getText()).toEqual(triage.contactErrorMessage);
            expect(form.errorMessages.get(11).getText()).toEqual(triage.emailErrorMessage);
            expect(form.errorMessages.get(12).getText()).toEqual(triage.telephoneErrorMessage);
        });

    });

    describe('Navigate to previous section', function () {

        it('Should navigate back to experience section', function () {
            triage.formBackButton.get(2).click();
            expect(triage.sectionHeaders.get(2).isDisplayed()).toBe(true);
        });

        it('Should navigate to contact details section', function () {
            triage.formNextButton.get(2).click();
            expect(triage.sectionHeaders.get(3).isDisplayed()).toBe(true);
        })

    });

    describe('submit form successfully', function () {

        it('should submit feedback', function () {
            form.nameInputField.sendKeys(settings.user.name);
            form.emailInputField.sendKeys(settings.user.email);
            form.telephoneInputField.sendKeys(settings.user.telephone);
            triage.formNextButton.get(3).click();
            expect(triage.successPageHeader.getText()).toEqual('Your application has been sent.');
            expect(browser.getCurrentUrl()).toContain('thanks');
        });
    })



});
