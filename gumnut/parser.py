from . import googlemaps as gm


def parse_id(url):
    page_name = url.split("/").pop()
    return int(page_name.split('.')[0])


def parse_description(scraped):
    try:
        return scraped.find(id='postingbody').get_text().replace('\n', ' ').strip()
    except AttributeError:
        return "No Address"


def parse_price(scraped):
    return int(scraped.find('span', class_='price').get_text().strip().lstrip("$"))


def parse_neighborhood(scraped):
    try:
        return scraped.find('small').get_text().strip().strip("()")
    except AttributeError:
        return "No Address"


def parse_title(scraped):
    return scraped.find('title').get_text().strip()


def parse_address(scraped):
    try:
        return scraped.find('div', class_='mapaddress').get_text().strip()
    except AttributeError:
        return "No Address"


def parse_time_to_work(scraped, work_coord, travel_method):
    try:
        map_tag = scraped.find('div', class_='viewposting').attrs
        orig_coord = float(map_tag['data-latitude']
                           ), float(map_tag['data-longitude'])
        return gm.get_travel_time(orig_coord, work_coord, travel_method)
    except AttributeError:
        return 0
