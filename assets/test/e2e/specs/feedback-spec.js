var settings = require('../settings/settings'),
    feedback = require('../settings/feedback'),
    form = require('../settings/form');


describe('list page', function() {

    beforeEach(function () {
        browser.ignoreSynchronization = true;
    });

    it('Should be on the feedback page', function() {
        browser.get(settings.navigate.feedback);
        expect(settings.pageHeader.getText()).toEqual('Help us improve this service');
        expect(form.errorMessages.get(0).getText()).toEqual('');
        expect(form.errorMessages.get(1).getText()).toEqual('');
        expect(form.errorMessages.get(2).getText()).toEqual('');
    });


    describe('Should not sent form', function () {

        it('should display all error messages, all fields empty', function () {
            settings.submitButton.click();
            expect(form.errorMessages.get(0).getText()).toEqual(feedback.nameErrorMessage);
            expect(form.errorMessages.get(1).getText()).toEqual(feedback.emailErrorMessage);
            expect(form.errorMessages.get(2).getText()).toEqual(feedback.feedbackErrorMessage);
        });

        it('Should display on 2 error messages', function () {
            form.nameInputField.sendKeys(settings.user.name);
            settings.submitButton.click();
            expect(form.errorMessages.get(0).getText()).toEqual('');
            expect(form.errorMessages.get(1).getText()).toEqual(feedback.emailErrorMessage);
            expect(form.errorMessages.get(2).getText()).toEqual(feedback.feedbackErrorMessage);
        });

        it('Should display on 1 error message', function () {
            form.emailInputField.sendKeys(settings.user.email);
            settings.submitButton.click();
            expect(form.errorMessages.get(0).getText()).toEqual('');
            expect(form.errorMessages.get(1).getText()).toEqual('');
            expect(form.errorMessages.get(2).getText()).toEqual(feedback.feedbackErrorMessage);
        });

        it('Should display on 2 error message', function () {
            form.emailInputField.clear();
            settings.submitButton.click();
            expect(form.errorMessages.get(0).getText()).toEqual('');
            expect(form.errorMessages.get(1).getText()).toEqual(feedback.emailErrorMessage);
            expect(form.errorMessages.get(2).getText()).toEqual(feedback.feedbackErrorMessage);
        });

    });


    describe('Should sent form', function() {

        it('Should sent feedback succesfully', function() {
            browser.get(settings.navigate.feedback);

            form.nameInputField.sendKeys(settings.user.name);
            form.emailInputField.sendKeys(settings.user.email);
            feedback.feedbackInputField.sendKeys(settings.user.message);
            settings.submitButton.click();
            expect(browser.getCurrentUrl()).toContain('thanks');
            expect(settings.pageHeader.getText()).toEqual('Your feedback has been sent');
        });

    });


});
