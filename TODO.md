# decisions
  - No images for now
  - Use Google Maps bc they'll have the best API, deal with rate limits etc later
    -  start with lat/lon?
  - use recurring plugins
  - worry about user data submissions later
  - Use the most basic version of everything to get a proof of Concept
    - non spatial DB
    - google maps input with lat/lon
    - recurring events plugin
    - Show, Event, Location
  - Later, store country, city, region
  - YOU CAN ONLY SUBMIT EVENTS VIA FB
      - use existing FB groups
      - track all events from comedy fb pages that have multiple events
      - add a 'flag' option for events to remove accident adds (parties, etc)


# API
  / events - all events
  / events/ country - events filtered by country
  / events/ country / region
  events/country/{region OR city}
  events/country/region/city

  - all endpoints can be filtered by
    - start time (defaults to datetime.now())
    - end-time (defaults to 4 hours from now)

  - /events can filter by longitude/latitude

# To Do
  - Add LINTERS!
  - add long/lat and start& end to URLs
  - Show points on google map
  - Save FB Pages from Events
    - parse events from pages
  - Read-only API
  - convert to GeoDjango?
  - Build React app

# Done
  - use signals to get the remaining Google Map data
    - save country, city, region, lat, lon


# Before Launch
  - secure DB (admin/pass)
  - CDN for API
  - CDN/Image Server (Imgix?)
    - do we have to save images ever, can we just use a CDN + FB images?
  - Environment variables
  - Google Analytics

# Concept
  - create one off and recurring events
  - events have location information (with google maps picker)
  - filter events by date/time & lat/long

#  questions
  - who can input events?
  - submit form?
  - import form?
  - confirm by admin to display in calendar?



# Proof Of Concept
  - input events using django admin (restricted users)



# later
  - input form
  - Upvote shows
  - FB import (meetup? Eventbrite)
  - Social Auth


# Adoption
   - Post to Craigslist and all event sites?
   - Sponsor Flyers

# Done
  - install NPM packages (instead of django-bower)
