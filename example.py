import gumnut as gn
import pandas as pd


if __name__ == '__main__':
    ex_search_params = {
        'max_price': 800,
        'hasPic': 1
    }

    work_coord = 40.756946, -73.985675

    legacy_listings = pd.read_csv('craigslistDB.csv')
    known_urls = legacy_listings['url']
    known_urls = []

    urls = gn.search(ex_search_params)
    new_listings = pd.concat((gn.read(url, work_coord=work_coord)
                             for url in urls if url not in known_urls), axis=0)

    listings = pd.concat([legacy_listings, new_listings])
    listings.to_csv("craigslistDB.csv", header=True,
                    index=False, encoding='utf-8')
