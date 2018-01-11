module.exports = {
    errorMessages: element.all(by.css('.form-group-error--message')),
    nameInputField: element.all(by.css('#id_contact_name')),
    emailInputField: element.all(by.css('#id_contact_email')),
    telephoneInputField: element.all(by.css('#id_contact_phone')),
};
