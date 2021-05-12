import requests
import json
import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

pp=pprint.PrettyPrinter(indent=4)

page_audi, page_ford, page_dodge, page_chevy, page_vw = 0,0,0,0,0



def download_inv(dealer, url):
    data[dealer]['Inventory'] = json.loads(requests.get(req[dealer][0]).content)

def download_facets(dealer, url):
    data[dealer]['Facets'] = json.loads(requests.get(req[dealer][1]).content)

def pull_data():
    req, data = {}, {}
    req['audi'] = [f'https://www.audigreenville.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory', f'https://www.audigreenville.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    req['ford'] = [f'https://www.fairwayford.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory',f'https://www.fairwayford.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    req['dodge'] = [f'https://www.bigododge.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory', f'https://www.bigododge.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    req['chevy'] = [f'https://www.kevinwhitaker.net/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory',f'https://www.kevinwhitaker.net/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    req['vw'] = [f'https://www.stevewhitevw.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory',f'https://www.stevewhitevw.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getFacets']

    dealers = ['audi', 'ford', 'dodge', 'chevy', 'vw']
    processes = []
    with ThreadPoolExecutor(max_workers=10) as executor:
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

data = pull_data()