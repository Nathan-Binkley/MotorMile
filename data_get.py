import requests
import json
import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

pp=pprint.PrettyPrinter(indent=4)

page_audi, page_ford, page_dodge, page_chevy, page_vw = 0,0,0,0,0

req = {}
data = {}



def download_inv(url, p=None):
    stuff = json.loads(requests.get(url, params = p).content)
    # print(stuff)
    return stuff

def download_facets(dealer, url):
    data[dealer]['Facets'] = json.loads(requests.get(req[dealer][1]).content)

def pull_data():
    data = {}

    # req['nissan'] = [f'www.google.com',f'https://www.crowngreenvillenissan.com/apis/widget/INDEX:inventory-search2/getFacets']


    req['ford'] = [f'https://www.fairwayford.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory',f'https://www.fairwayford.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    req['dodge'] = [f'https://www.bigododge.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory', f'https://www.bigododge.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    req['chevy'] = [f'https://www.kevinwhitaker.net/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory',f'https://www.kevinwhitaker.net/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    req['vw'] = [f'https://www.stevewhitevw.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory',f'https://www.stevewhitevw.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    dealers = ['audi', 'ford', 'dodge', 'chevy', 'vw', 'nissan']
    processes = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for current in dealers:
            data[current] = {'Inventory':{}, 'Facets':{}}
            processes.append(executor.submit(download_inv, current, req[current][0]))
            processes.append(executor.submit(download_facets, current, req[current][1]))

        

        with open(f"data/{current}_readable.json", 'w') as f:
            json.dump(data[current], f, indent=4)
        with open(f"data/{current}.min.json", 'w') as f:
            json.dump(data[current], f)

    with open("data/dealers_readable.json", "w") as f: 
        json.dump(data, f, indent=4)
    with open("data/dealers.min.json", "w") as f:
        json.dump(data, f)

    return data

def get_audi_inv():
    audi = [f'https://www.audigreenville.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory', f'https://www.audigreenville.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    data = []
    i = 0
    with open("data/audi.min.json", "r") as f:
        a = json.load(f)

    processes = []
    page_size = a["Inventory"]['pageInfo']['pageSize']
    total_count = a["Inventory"]['pageInfo']['totalCount']
    print(f"Page size {page_size}")
    print(f"total_count {total_count}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        url = audi[0]
        while page_size * i < total_count: #dynamic page size scrolling
            payload={'start':page_size * i} #handle scrolling pages

            processes.append(executor.submit(download_inv, audi[0], payload)) #append to processes. Results end up in that list. think promise in JS
            i += 1 #index loop to dynamic load web pages

        for i, dat in enumerate(processes):
            
            try:
                print(i, 'RESULT')
            except Exception as e:
                print(e)
            data.append(dat.result())
    return data

def clean_up_audi(data):
    final = []
    total_count = 0
    for dat in data:
        total_count += len(dat)
        final.extend(dat['inventory'])
    print(total_count)
    return final

# data = pull_data()
def get_and_store_audi():
    audi = get_audi_inv()
    audi = clean_up_audi(audi)

    with open("data/audi_inv.json", 'w') as f:
        json.dump(audi, f, indent=4) #File storage

def get_audi_local():
    with open("data/audi_inv.json", 'r') as f:
        return json.load(f) #File storage