var validationMessages = (function () {

    var messages = {
        'company': {
            'name': 'Provide your legal company name',
            'search': 'Please search for your company name.',
            'number': 'Enter your company number or if you don\'t have one tick the box below',
            'no_number': 'If you don\'t have a company number please tick this box.',
            'postcode' : 'Tell us the postcode where your business is based',
            'website': 'Provide a link to where we can see your products online '
        },
        'business': {
            'turnover': 'Select an option which best describes your turnover',
            'sku': 'Provide the total number of stock keeping units',
            'trademark': 'Select yes if your products are trademarked'
        },
        'experience': {
            'export': 'Select an option which best describes your experience in selling online abroad',
            'introduction': 'Write a few paragraphs about your business and products'
        },
        'contact' :{
            'name': 'Enter the name of the person we should talk to',
            'email': 'Provide a valid email address',
            'phone': 'Enter a valid phone number'
        }
    };


    return {
        messages: messages
    };

})();