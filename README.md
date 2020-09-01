# Django Star Wars

## App features - general description
* allows to collect, resolve and inspect information about characters
in the Star Wars universe from the SWAPI
* API used: https://swapi.co/api/people/

## App features - detailed description
* ability to download the latest complete dataset of characters as CSV file
* ability to process large amounts of data

## Development notes

* prod version uses development server
* simple GUI

# Notes on how the app can be improved
* use async server to handle multiple clients
* improve caching mechanism -> maybe Redis?
* cache also /people endpoint
* properly include all the necessary css/js files to be served
* use template inheritance
* add Dockerfile so it can be easily containerized
* refactor -> not the best design yet, but works
* add the tests