var url = process.env.TRAVIS ? 'https://contact-us.export.staging.uktrade.io' : 'http://contact.trade.great:8009';

module.exports = {
    navigate: {
        feedback: url+'/feedback/selling_online_overseas/',
        triage: url+'/triage/asda/?market=ebay'
    },
    submitButton: element.all(by.css('button[type=submit]')),
    pageHeader: element(by.css('h1.heading-xlarge')),
    user: {
        name: 'John Doe',
        email: 'johndoe@test.com',
        message: 'This a test messsage',
        website: 'www.example.com',
        company: 'test ltd',
        companyPostCode: 'se17 4we',
        Skus: 10,
        businessPitch: 'This is a pitch',
        telephone: 999999999
    }
};
