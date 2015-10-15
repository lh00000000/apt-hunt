import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import pandas as pd
import nltk
import simplejson
import urllib

maps_api_key = ''
work_coord = 40.756946, -73.985675
default_search_params = {
    'max_price': 800,
    'hasPic': 1
}


def get_listing_urls(search_params=default_search_params, city="newyork", listing_suffix="brk/roo"):

    search_url = 'http://%s.craigslist.org/search/%s' % (city, listing_suffix)
    resp = requests.get(search_url, params=search_params, timeout=100)
    resp.raise_for_status()    # <- no-op if status==200

    parsed = BeautifulSoup(resp.content, 'html.parser',
                           from_encoding=resp.encoding)

    city_url = "https://%s.craigslist.org" % (city)
    return (city_url + url.attrs['href'] for url in parsed.find_all('a', class_='i') if not url.attrs['href'].startswith('//'))
    # craigslist mixes in some listings from surroudning areas. they start
    # like //newyork.cl.org/search/HELL


def get_transit_time(orig_coord, dest_coord):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=transit&language=en-EN&key={2}".format(
        str(orig_coord), str(dest_coord), maps_api_key)
    result = requests.get(url, timeout=30).json()
    transit_time = result['rows'][0]['elements'][0]['duration']['value']
    return transit_time  # in seconds


def scrape_listing(url):
    try:
        resp = requests.get(url, timeout=10)
        return BeautifulSoup(resp.content, 'html.parser', from_encoding=resp.encoding)
    except requests.exceptions.ReadTimeout:
        return ""


def get_id(url):
    page_name = url.split("/").pop()
    return int(page_name.split('.')[0])


def get_description(scraped):
    try:
        return scraped.find(id='postingbody').get_text().replace('\n', ' ').strip()
    except AttributeError:
        return "No Address"


def get_price(scraped):
    return int(scraped.find('span', class_='price').get_text().strip().lstrip("$"))


def get_neighborhood(scraped):
    try:
        return scraped.find('small').get_text().strip().strip("()")
    except AttributeError:
        return "No Address"


def get_title(scraped):
    return scraped.find('title').get_text().strip()


def get_address(scraped):
    try:
        return scraped.find('div', class_='mapaddress').get_text().strip()
    except AttributeError:
        return "No Address"


def get_time_to_work(scraped):
    try:
        map_tag = scraped.find('div', class_='viewposting').attrs
        orig_coord = float(map_tag['data-latitude']
                           ), float(map_tag['data-longitude'])
        return get_transit_time(orig_coord, work_coord)
    except AttributeError:
        return 0


def get_info(url):
    scraped = scrape_listing(url)

    info = {}
    info["url"] = url
    info["id"] = get_id(url)

    info["description"] = get_description(scraped)
    info["price"] = get_price(scraped)
    info["neighborhood"] = get_neighborhood(scraped)
    info["title"] = get_title(scraped)
    info["address"] = get_address(scraped)
    info["toWork"] = get_time_to_work(scraped) 

    return pd.DataFrame([info])


if __name__ == '__main__':
        
    legacy_listings = pd.read_csv('craigslistDB.csv')
    known_ids = legacy_listings['id']

    urls = get_listing_urls('https://newyork.craigslist.org/search/brk/roo')
    new_listings = pd.concat(get_info(url) for url in urls if get_id(url) not in known_ids)

    listings = pd.concat([legacy_listings, new_listings])
    listings.to_csv("craigslistDB.csv", header=True, index=False, encoding='utf-8')





