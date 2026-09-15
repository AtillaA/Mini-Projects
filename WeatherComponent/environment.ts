/** Application Config */
export const environment = {
    /** WeatherAPI key. Retrieved from https://www.weatherapi.com/ */
    weatherApiKey: 'ENTER_KEY_HERE',

    /** Base URL of the WeatherAPI REST service */
    weatherApiBaseUrl: 'https://api.weatherapi.com/v1',

    /** 'metric' -> °C / km/h, 'imperial' -> °F / mph. */
    units: 'metric' as 'metric' | 'imperial',

    /**
     * validity period of a fetched weather data
     * a repeat search for the same city is answered from the cache
     * the record is discarded and re-fetched once expired
     */
    cacheTtlMs: 60 * 60 * 1000,

    /** idle time after the last keystroke before the app reacts */
    debounceMs: 350,

    /**
     * shortest input that may be sent to the online city-validation endpoint
     */
    minOnlineValidationLength: 4
};
