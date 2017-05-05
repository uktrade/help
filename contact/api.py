import requests
from functools import lru_cache

from django.http import JsonResponse
from django.conf import settings

from brake.decorators import ratelimit


@ratelimit(rate='30/m', block=True)
def company_detail_api(request):
    query = request.GET.get('q')
    return _query_companies_house(query)


@lru_cache(maxsize=64)
def _query_companies_house(query):
    url = 'https://api.companieshouse.gov.uk/search/companies'
    headers = {'content-type': 'application/json'}
    data = []

    try:
        response = requests.get(url, params={'q': query, 'items_per_page': 10},
                                auth=(settings.COMPANIES_HOUSE_API_KEY, ''),
                                headers=headers)

        status_code = response.status_code

        if status_code == 200:
            for item in response.json()['items']:
                company_data = [item['title'], item['company_number']]
                try:
                    company_data.append(item['address']['postal_code'])
                except KeyError:
                    company_data.append('')

                data.append(company_data)
    except:
        status_code = 500

    return JsonResponse({'companies': data}, status=status_code)
