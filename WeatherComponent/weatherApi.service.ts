import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, map, throwError } from 'rxjs';

import { environment } from './environment';
import type { data } from './weatherDetails.component';

/** Shape of the parts of GET /v1/current.json used */
interface CurrentWeatherResponse {
    location: { name: string; region: string; country: string };
    current: {
        temp_c: number;
        temp_f: number;
        wind_kph: number;
        wind_mph: number;
        humidity: number;
    };
}

/** Shape of one entry of GET /v1/search.json */
interface LocationSearchResponse {
    name: string;
    region: string;
    country: string;
}

/**
 * Every HTTP conversation with WeatherAPI
 * Rest of the app `data` records and strings
 */
@Injectable({ providedIn: 'root' })
export class WeatherApiService {
    constructor(private readonly http: HttpClient) {}

    /** False until an API key has been filled */
    get isConfigured(): boolean {
        return environment.weatherApiKey.trim().length > 0;
    }

    /**
     * GET /v1/current.json - live conditions for one city
     * Mapped to `data` record shape the component renders
     */
    getCurrentWeather(city: string): Observable<data> {
        const params = new HttpParams()
            .set('key', environment.weatherApiKey)
            .set('q', city)
            .set('aqi', 'no');

        return this.http
            .get<CurrentWeatherResponse>(`${environment.weatherApiBaseUrl}/current.json`, { params })
            .pipe(
                map((response) => this.toRecord(response)),
                catchError((error) => this.toFriendlyError(error))
            );
    }

    /**
     * GET /v1/search.json - WeatherAPI's own location autocomplete
     * Returns the matching location names
     */
    searchLocations(term: string): Observable<string[]> {
        const params = new HttpParams()
            .set('key', environment.weatherApiKey)
            .set('q', term);

        return this.http
            .get<LocationSearchResponse[]>(`${environment.weatherApiBaseUrl}/search.json`, { params })
            .pipe(
                map((matches) => (matches || []).map((match) => match.name)),
                catchError((error) => this.toFriendlyError(error))
            );
    }

    private toRecord(response: CurrentWeatherResponse): data {
        const metric = environment.units === 'metric';
        const { location, current } = response;

        return {
            name: location.name,
            temperature: metric
                ? `${Math.round(current.temp_c)}° C`
                : `${Math.round(current.temp_f)}° F`,
            wind: metric
                ? `${Math.round(current.wind_kph)}Kmph`
                : `${Math.round(current.wind_mph)}Mph`,
            humidity: `${current.humidity}%`
        };
    }

    /**
     * WeatherAPI reports problems as {error: {code, message}} with a 4xx status
     * Code 1006 ("No matching location found") flagged separately
     */
    private toFriendlyError(error: HttpErrorResponse): Observable<never> {
        const apiCode: number | undefined = error.error?.error?.code;
        const apiMessage: string | undefined = error.error?.error?.message;

        if (apiCode === 1006) {
            return throwError(() => new WeatherApiError('No matching location found.', true));
        }
        if (apiCode === 2006 || apiCode === 2007 || apiCode === 2008 || error.status === 401 || error.status === 403) {
            return throwError(
                () => new WeatherApiError(apiMessage || 'The WeatherAPI key was rejected.')
            );
        }
        if (error.status === 0) {
            return throwError(
                () => new WeatherApiError('Could not reach WeatherAPI - check your connection.')
            );
        }
        return throwError(
            () => new WeatherApiError(apiMessage || 'Weather lookup failed. Please try again.')
        );
    }
}

// Error type/msg shown in UI
export class WeatherApiError extends Error {
    constructor(message: string, readonly isUnknownLocation = false) {
        super(message);
        this.name = 'WeatherApiError';
    }
}
