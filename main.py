import requests

from config import TOKEN


base_url = f'https://api.telegram.org/bot{TOKEN}/'
command = 'getMe'

response = requests.get(base_url + command)

print(response.json())
