Minimal craiglist apartment listing scraper.

To get commute time estimates (optional):
  export $GM_APIKEY=your google maps api key 

Dataframe columns:
url: url of posting
id: craigslist posting id
description: description of listing
price: listed price
neighborhood: sublocation. could be town where you are. i wrote this looking for a place in brooklyn.
title: title of listing
address: address, if the poster put one there. stored as a string (i.e. will get the meaningless impossible street corners brokers put here )
toWork: number of seconds google maps estimates to get to work (departing time defaulting to now)

Hope this could give someone a start on doing this properly. I found a place the day after I started writing this so I didn't put as much time as I wanted to in.*

Name comes from this http://metro.co.uk/2014/12/09/this-advert-for-gumnut-the-angry-koala-just-won-the-internet-4980840/

* I mainly wanted this to be able to feed listings through a spam classifier. Wouldn't that be great? Wow I'm so glad you agree! What's that? You said you'll implement that yourself? Fantastic!
