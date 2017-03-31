import requests

initial_data = {
    'contact_name': 'Spam Eggs',
    'contact_email': 'spam@example.com',
    'content': 'testing contact form',
    'service': 'test',
    'originating_page': 'google.com'
}

response201 = requests.Response()
response201.status_code = 201
