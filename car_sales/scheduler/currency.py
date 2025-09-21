import requests
from .models import ExchangeRate
def get_usd_to_uah():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&json"
    resp = requests.get(url).json()
    rate=resp[0]["rate"]
    ExchangeRate.objects.update_or_create(currency='USD',defaults={'rate':rate})
    return rate