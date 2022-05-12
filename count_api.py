#importamos la libreria que permitira realizar la peticion a la API
import requests
from collections import Counter

# definimos la url de la API
response_api = requests.get('https://api.disneyapi.dev/characters')

# realizamos una exploracion de los items de la API
for item in response_api.json():
    print(item)

# extraemos el numero de paginas que posee la API
# print(response_api.json()['totalPages'])

pages = response_api.json()['totalPages']

counts = 0
query = 0

for page in range(1, pages+1):
    response_api = requests.get('https://api.disneyapi.dev/characters?page=' + str(page))
    # cargamos los datos de cada pagina y los utilizamos para contar los items
    for item in response_api.json()['data']:
        
        query = item['name'].lower().split(' ').count(('princess')) + query
        counter = Counter(item['name'])
        
        # print(counter['a'] + counter['e'] + counter['i'] + counter['o'] + counter['u'])
        counts = counts + counter['a'] + counter['e'] + counter['i'] + counter['o'] + counter['u'] 
        
        # print("pagina", page)
        # print(counts)
        # print(query)
print(f"final count:{counts}")
print(f"final query:{query}")





