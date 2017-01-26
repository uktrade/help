import requests
from django.http import JsonResponse

initial_data = {
    'contact_name': 'Spam Eggs',
    'contact_email': 'spam@example.com',
    'content': 'testing contact form',
    'service': 'test',
    'originating_page': 'google.com'
}

response201 = requests.Response()
response201.status_code = 201

response200 = requests.Response()
response200.status_code = 200

response400 = JsonResponse({'error': "an error occurred"}, status=400)
