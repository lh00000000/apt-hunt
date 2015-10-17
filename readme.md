Minimal craiglist apartment listing scraper.

To get commute time estimates (optional):
  export $GM_APIKEY=your google maps api key 

Dataframe columns:<br>
url: url of posting<br>
id: craigslist posting id<br>
description: description of listing<br>
price: listed price<br>
neighborhood: sublocation. could be town where you are. i wrote this while looking for a place in brooklyn.<br>
title: title of listing<br>
address: address, if the poster put one there. stored as a string (i.e. will get the meaningless impossible street corners brokers put here)<br>
toWork: number of seconds google maps estimates to get to work (departing time defaulting to now)<br>

Hope this could give someone a start on doing this properly. I found a place the day after I started writing this so I didn't put as much time as I wanted to in.*

Name comes from this http://metro.co.uk/2014/12/09/this-advert-for-gumnut-the-angry-koala-just-won-the-internet-4980840/

* I mainly wanted this to be able to feed listings through a spam classifier. Wouldn't that be great? Wow I'm so glad you agree! What's that? You said you'll implement that yourself? Fantastic!
