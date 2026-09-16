# Weather Component
-------------------
Weather component application. Check current weather in a quried city.


## Features:
------------
An Angular 18 Weather querying application that renders a single search card. The user types a city name and gets its live temperature, wind, humidity and a condition icon. 

Keystrokes feed an RxJS pipeline that waits for an interval, ignores repeats, and cancels any lookup the user has already typed in the past in order to ensure that a query is only resolved once the input has settled. 

Before spending a network call, the typed text has to pass a two-tier city check: 
    1. An offline dictionary of 32,677 city names — every city on earth with a population of 15,000 or more, derived from the GeoNames cities15000 dataset by tools/build-city-index.mjs, restricted to Latin-script names and shipped as a 328 KB asset — which is fetched once, held in memory as a Set, and answers instantly without touching the network.
    
    2. Only for text that the dictionary does not recognise, and only when it is at least four characters long, WeatherAPI's own location search is triggered. Counts the input as a city only if a returned location matches it exactly, so a partial name is rejected rather than silently resolved to some larger city. 
    
Both tiers compare names case- and accent-insensitive. Each online verdict is memoised so the same text is never re-validated. Once a name is confirmed, API service does the app call WeatherAPI's current-conditions endpoint, mapping the response into a display record whose units follow a metric/imperial setting in environment.

Failures are translated into distinct user-facing states rather than raw errors: an unrecognised location shows "No Results Found", a rejected or missing API key and an unreachable network each get their own message, and anything else falls back to a generic retry message. 

Successful fetches go through a cache layer that keeps records in an in-memory map mirrored into localStorage, so a repeat search for the same city within an hour is redrawn from the cache and costs no API call, and the cache survives a page reload; entries are filed under both the typed text and the canonical name WeatherAPI returns, expired or malformed ones are discarded whenever they're read or restored, every storage access is written defensively so that a blocked or corrupt store degrades to an in-memory cache instead of breaking the app, and records still fresh from an earlier visit are replayed to the parent component on startup to repopulate its weather array.

The component has the following functionalities:
    - An array of objects is passed as a prop to the component, where each object is a weather record for a single city. The object has 4 properties:
        • name: The name of the city. [STRING]
        • temperature: The temperature in the city. [STRING]
        • wind: The wind in the city. [STRING]
        • humidity: The humidity in the city. [STRING]

    - There is an input field for the city name where the user can type the name of a city to search the weather data for. (case-insensitive)
    - If data exists for the typed input, renders the weather details <div> as below, inside <div data-test-id="weather-details">.
        • <span data-test-id="output-temperature">{temperature}</span>, where {temperature} is the value from the weather record.
        • <div data-test-id="output-wind>Wind: {wind}</div>, where {wind} is the value from the weather record.
        • <div data-test-id="output-humidity>Humidity: {humidity}</div>, where {humidity} is the value from the weather record.
    
    - If no data exists for the typed input, does not render the weather details <div>, but instead renders <div data-test-id="no-results">No Results Found</div>.
    - At component render, since nothing is typed, does not render the above two <div> elements ("weather-details" and "no-results").




## Development Environment
--------------------------
Node 18.19+/20.11+/22+
npm


## Getting Started
------------------
1. Install dependencies (npm install - 847 packages)
2. Start the server Compile TypeScript (npm start - dev server at http://localhost:4200)
