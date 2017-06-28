module.exports = {
    benefitsSection: element(by.css('.form-intro-content')),
    sectionHeaders: element.all(by.css('.form-steps-header')),
    benefitsSectionButton: element(by.css('.form-intro-button')),
    companyNameInputField: element(by.css('#id_company_name')),
    companyList: element(by.css('#id_company_name +ul')).all(by.tagName('li a')),
    companySearchButton: element(by.css('.search-companies')),
    companyNumberInputField: element(by.css('#id_company_number')),
    descriptionInputField: element(by.css('#id_description')),
    skuInputField: element(by.css('#id_sku_count')),
    turnoverInputField: element(by.css('.selection-button-radio[for="id_turnover_0_0"]')),
    trademarkInputField: element(by.css('.selection-button-radio[for="id_trademarked_0_0"]')),
    soldOutsideInputField: element(by.css('.selection-button-radio[for="id_experience_0_0"]')),
    companyPostCodeInputField: element(by.css('#id_company_postcode')),
    successPageHeader: element(by.css('.form-success-header')),
    companyWebsiteInputField: element(by.css('#id_website_address')),
    formNextButton: element.all(by.css('.form-tab-button .button')),
    formBackButton: element.all(by.css('.form-tab-button .form-tab-back')),
    companyNameErrorMessage: 'Enter your legal company name and use search',
    companyWebsiteErrorMessage: 'Provide a link to where we can see your products online',
    companyTurnoverErrorMessage: 'Select an option which best describes your turnover',
    companySkuErrorMessage: 'Provide the total number of stock keeping units',
    companyTradeMarkErrorMessage: 'Select yes if your products are trademarked',
    soldProductErrorMessage: 'Select an option which best describes your experience in selling online abroad',
    contactErrorMessage: 'Enter the name of the person we should talk to',
    emailErrorMessage: 'Provide a valid email address',
    telephoneErrorMessage: 'Enter a valid phone number containing only numbers and without spaces',
    descriptionErrorMessage: 'Write a few paragraphs about your business and products',
};