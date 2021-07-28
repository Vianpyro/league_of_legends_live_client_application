import requests
from requests.models import HTTPBasicAuth

request = requests.get(
    'https://localhost:54728/liveclientdata/activeplayer', verify=False,
    auth=HTTPBasicAuth('riot', 'CEepAMQrkRAb1jBWRyLeRQ')
)
print(request)
