import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import pandas as pd
import nltk
import simplejson, urllib

maps_api_key=''
work_coord = 40.756946, -73.985675

def get_urls(baseurl='https://newyork.craigslist.org/search/brk/roo'):
  search_params = {
    'max_price': 800
  }

  base = 'http://newyork.craigslist.org/search/brk/roo'
  resp = requests.get(base, params=search_params, timeout=100)
  resp.raise_for_status()  # <- no-op if status==200

  parsed = BeautifulSoup(resp.content, 'html.parser', from_encoding=resp.encoding)

  return ("https://newyork.craigslist.org" + url.attrs['href'] for url in parsed.find_all('a', class_='i') if not url.attrs['href'].startswith('//'))
  # craigslist mixes in some listings from surroudning areas. they start like //newyork.cl.org/search/HELL

def get_transit_time(orig_coord, dest_coord):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=transit&language=en-EN&key={2}".format(str(orig_coord),str(dest_coord),maps_api_key)
    result = requests.get(url, timeout=30).json()
    transit_time = result['rows'][0]['elements'][0]['duration']['value']
    return transit_time

def scrape_listing(url):
  try:
    resp = requests.get(url, timeout=10)
    return BeautifulSoup(resp.content, 'html.parser',from_encoding=resp.encoding)
  except requests.exceptions.ReadTimeout:
    return ""

def get_id(url):
  page_name = url.split("/").pop()
  return int(page_name.split('.')[0])

def get_description(parsed):
  try:
    return parsed.find(id='postingbody').get_text().replace('\n', ' ').strip()
  except AttributeError:
    return "No Address"

def get_price(parsed):
  return int(parsed.find('span', class_='price').get_text().strip().lstrip("$"))

def get_neighborhood(parsed):
  try: 
    return parsed.find('small').get_text().strip().strip("()")
  except AttributeError:
    return "No Address"

def get_title(parsed):
  return parsed.find('title').get_text().strip()


def get_address(parsed):
  try:
    return parsed.find('div', class_='mapaddress').get_text().strip()
  except AttributeError:
    return "No Address"

def get_time_to_work(parsed):
  try:
    map_tag = parsed.find('div', class_='viewposting').attrs
    orig_coord = float(map_tag['data-latitude']), float(map_tag['data-longitude'])
    return get_transit_time(orig_coord, work_coord)
  except AttributeError:
    return 0

def get_info(url, blacklisted_ids = []):
  info = {}
  info["url"] = url
  info["id"] = get_id(url)

  if info["id"] not in blacklisted_ids:
    
    parsed = scrape_listing(url)
    info["description"] = get_description(parsed)
    info["price"] = get_price(parsed)
    info["neighborhood"] = get_neighborhood(parsed)
    info["title"] = get_title(parsed)
    info["address"] = get_address(parsed)
    
    #info["toPABT"] = get_time_to_work(parsed)

    return pd.DataFrame([info])
  else:
    return listings[info["id"]]


legacy = pd.read_csv('craigslistDB.csv')
known_ids = legacy['id']

urls = get_urls('https://newyork.craigslist.org/search/brk/roo')
listings = pd.concat(get_info(url, blacklisted_ids = known_ids) for url in urls)
listings.to_csv("craigslistDB.csv", header=True, index=False, encoding='utf-8')
