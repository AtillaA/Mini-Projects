import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, map, of, shareReplay, switchMap } from 'rxjs';

import { environment } from './environment';
import { WeatherApiService } from './weatherApi.service';

/**
 * Weather request gate:
 *
 *   1. An offline dictionary (assets/city-index.txt) of every city with a population of 15,000+
 *      32,677 names generated from the GeoNames cities15000 dataset by tools/build-city-index.mjs.
 *      Fetched once, turned into a Set, and answers in O(1) with no network traffic.
 *
 *   2. For all that dict does not recognise - 
 *      The typed text counts as a full city name only if one of the returned locations matches it exactly
 *      Thus, a prefix is still rejected.
 *
 *   Both tiers compare normalised strings - case and accent insensitive -
 */
@Injectable({ providedIn: 'root' })
export class CityValidatorService {
    private index$: Observable<Set<string>> | null = null;

    /** to recall finalised strings to prevent the check of same text */
    private readonly onlineVerdicts = new Map<string, boolean>();

    constructor(
        private readonly http: HttpClient,
        private readonly weatherApi: WeatherApiService
    ) {}

    /** Identical to the normalise() in tools/build-city-index.mjs to match lookup on both sides */
    static normalise(value: string): string {
        return (value || '')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .toLowerCase()
            .replace(/\s+/g, ' ')
            .trim();
    }

    /** True if `term` is the complete name of a city */
    isCompleteCityName(term: string): Observable<boolean> {
        const needle = CityValidatorService.normalise(term);
        if (!needle) {
            return of(false);
        }

        return this.loadIndex().pipe(
            switchMap((index) => {
                if (index.has(needle)) {
                    return of(true);
                }
                return this.confirmOnline(needle);
            })
        );
    }

    /** Tier 1: fetch the offline dictionary once and keep it in memory */
    private loadIndex(): Observable<Set<string>> {
        if (!this.index$) {
            this.index$ = this.http.get('assets/city-index.txt', { responseType: 'text' }).pipe(
                map((text) => {
                    const names = new Set<string>();
                    for (const line of text.split('\n')) {
                        const name = line.trim();
                        if (name) {
                            names.add(name);
                        }
                    }
                    return names;
                }),
                // A missing or unreadable asset must not break the app - tier 2
                catchError(() => of(new Set<string>())),
                shareReplay({ bufferSize: 1, refCount: false })
            );
        }
        return this.index$;
    }

    /** Tier 2: ask WeatherAPI whether this exact name resolves to a location */
    private confirmOnline(needle: string): Observable<boolean> {
        if (needle.length < environment.minOnlineValidationLength || !this.weatherApi.isConfigured) {
            return of(false);
        }

        const remembered = this.onlineVerdicts.get(needle);
        if (remembered !== undefined) {
            return of(remembered);
        }

        return this.weatherApi.searchLocations(needle).pipe(
            map((names) =>
                names.some((name) => CityValidatorService.normalise(name) === needle)
            ),
            // A failed validation lookup should not surface as a weather error
            catchError(() => of(false)),
            map((verdict) => {
                this.onlineVerdicts.set(needle, verdict);
                return verdict;
            })
        );
    }
}
