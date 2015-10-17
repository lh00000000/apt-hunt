import requests
from bs4 import BeautifulSoup
from . import parser as p
import pandas as pd

maps_api_key = ''



def search(search_params, city="newyork", listing_suffix="brk/roo"):

    search_url = 'http://%s.craigslist.org/search/%s' % (city, listing_suffix)
    resp = requests.get(search_url, params=search_params, timeout=100)
    resp.raise_for_status()    # <- no-op if status==200

    parsed = BeautifulSoup(resp.content, 'html.parser',
                           from_encoding=resp.encoding)

    city_url = "https://%s.craigslist.org" % (city)
    return (city_url + url.attrs['href'] for url in parsed.find_all('a', class_='i') if not url.attrs['href'].startswith('//'))
    # craigslist mixes in some listings from surroudning areas. they start
    # like //newyork.cl.org/search/HELL


def read(url, work_coord=None, travel_method="transit"):

    resp = requests.get(url, timeout=10)
    scraped = BeautifulSoup(resp.content, 'html.parser',
                            from_encoding=resp.encoding)

    info = {}
    info["url"] = url
    info["id"] = p.parse_id(url)

    info["description"] = p.parse_description(scraped)
    info["price"] = p.parse_price(scraped)
    info["neighborhood"] = p.parse_neighborhood(scraped)
    info["title"] = p.parse_title(scraped)
    info["address"] = p.parse_address(scraped)
    if work_coord:
        info["toWork"] = p.parse_time_to_work(scraped, work_coord, travel_method)

    return pd.DataFrame([info])
