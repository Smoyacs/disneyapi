#importamos la libreria que permitira realizar la peticion a la API
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# definimos la url de la API
response_api = requests.get('https://api.disneyapi.dev/characters')
#Número de páginas
pages = response_api.json()['totalPages']

#seteamos todas las urls
urls = []

for page in range(1,pages+1):
    urls.append('https://api.disneyapi.dev/characters?page='+str(page))


# trabajadores
MAX_WORKERS = 30

#obtencion de urls
def get_url(url):
    return requests.get(url)

#obtencion de datos
def exec_requests():
    inicio = datetime.now()
    # de manera asincrona obtenemos las urls (30 workers)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        #asignacion de worker a la url
        response_list = list(pool.map(get_url,urls))
    paginasWorker = []
    for index,response in enumerate(response_list):
        paginasWorker.append(response.json())
    end = datetime.now()
    time = end-inicio
    return paginasWorker,time

def get_items(paginasWorker):
    items = []
    #
    for index,pagina in enumerate(paginasWorker):
        for pelicula in pagina['data']:
            items.append(pelicula['name'])
    return items

def get_repeated_princesses(items):
    princess_count = 0
    for p in items:
        for name in p.split(" "):
            if(name.lower() == "princess"):
                princess_count+=1
    return princess_count

def get_vocales(items):
    vocales_count = 0
    for item in items:
        for name in item.lower().split(" "):
            for letra in name:
                if(letra=="a" or letra=="o" or letra=="i" or letra=="e" or letra=="u"):
                    vocales_count+=1
    return vocales_count


paginasWorker,tiempo = exec_requests()
items = get_items(paginasWorker)

print("Numero de veces que se repite princess: {}".format(get_repeated_princesses(items)))
print("Numero de vocales: {}".format(get_vocales(items)))
print("Tiempo de demora en request",tiempo)
print("Numero de paginas: {}".format(len(paginasWorker)))