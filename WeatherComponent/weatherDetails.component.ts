import {Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import { EMPTY, Observable, Subject, catchError, debounceTime, distinctUntilChanged, switchMap, takeUntil, tap } from 'rxjs';

import { environment } from './environment';
import { CityValidatorService } from './cityValidator.service';
import { WeatherApiError, WeatherApiService } from './weatherApi.service';
import { WeatherCacheService } from './weatherCache.service';

/** what the card is currently showing */
export type SearchStatus =
    | 'idle'      // nothing typed - render neither block
    | 'loading'   // a real city was recognised, its weather is on the way
    | 'ready'     // weather details available
    | 'unknown'   // not a (complete) city name - render "No Results Found"
    | 'error';    // the lookup itself failed

@Component({
    selector: 'weather-details',
    templateUrl: './weatherDetails.component.html',
    styleUrls: ['./weatherDetails.component.scss']
})

export class WeatherDetails implements OnInit, OnDestroy {
    /**
     * weather record legacy
     * holds in cache and grows as searches resolve
     * each record is emitted through `weatherLoaded`
     * WeatherCacheService decides whether a search costs an API call
     */
    @Input() weatherData: data[] = [];

    /** emits fresh fetches so the parent can add it to the array */
    @Output() weatherLoaded = new EventEmitter<data>();

    /** raw text currently typed (trimmed) */
    searchTerm = '';

    /** matching weather record or null when there is no match */
    result: data | null = null;

    status: SearchStatus = 'idle';

    errorMessage = '';

    /** Keystrokes - before debouncing */
    private readonly terms$ = new Subject<string>();

    private readonly destroyed$ = new Subject<void>();

    constructor(
        private readonly weatherApi: WeatherApiService,
        private readonly cityValidator: CityValidatorService,
        private readonly weatherCache: WeatherCacheService
    ) {}

    ngOnInit() {
        // records cached by an earlier visit are still valid for up to an hour
        for (const record of this.weatherCache.freshRecords()) {
            this.weatherLoaded.emit(record);
        }

        this.terms$
            .pipe(
                debounceTime(environment.debounceMs),
                distinctUntilChanged(),
                // switchMap cancels the previous lookup
                switchMap((term) => this.resolve(term)),
                takeUntil(this.destroyed$)
            )
            .subscribe();
    }

    ngOnDestroy() {
        this.destroyed$.next();
        this.destroyed$.complete();
    }

    /**
     * called on every keystroke
     * clearing the input takes effect immediately
     * else is handed to the debounced pipeline above
     */
    search(value: string) {
        this.searchTerm = (value || '').trim();

        if (!this.searchTerm) {
            this.reset();
        }

        this.terms$.next(this.searchTerm);
    }

    /**
     * one debounced search: serve it from the array if we already have it
     * otherwise confirm the text is a complete city name and only then spend an API call
     */
    private resolve(term: string): Observable<unknown> {
        if (!term) {
            this.reset();
            return EMPTY;
        }

        // a city fetched within the last hour is redrawn from the cache
        const cached = this.weatherCache.get(term);
        if (cached) {
            this.show(cached);
            return EMPTY;
        }

        if (!this.weatherApi.isConfigured) {
            this.fail('Add your WeatherAPI key to environment.ts to load live weather.');
            return EMPTY;
        }

        this.result = null;
        this.status = 'loading';

        return this.cityValidator.isCompleteCityName(term).pipe(
            switchMap((isCity) => {
                if (!isCity) {
                    // not a city or only part of one - no API call is made
                    this.result = null;
                    this.status = 'unknown';
                    return EMPTY;
                }
                return this.weatherApi.getCurrentWeather(term).pipe(
                    tap((record) => this.accept(term, record))
                );
            }),
            catchError((error: unknown) => {
                if (error instanceof WeatherApiError && error.isUnknownLocation) {
                    this.result = null;
                    this.status = 'unknown';
                } else {
                    this.fail(
                        error instanceof Error ? error.message : 'Weather lookup failed.'
                    );
                }
                return EMPTY;
            })
        );
    }

    /** a record came back: cache it - display - hand it to array */
    private accept(term: string, record: data) {
        this.weatherCache.set(term, record);
        this.show(record);
    }

    private show(record: data) {
        this.result = record;
        this.status = 'ready';
        this.weatherLoaded.emit(record);
    }

    private fail(message: string) {
        this.result = null;
        this.errorMessage = message;
        this.status = 'error';
    }

    private reset() {
        this.result = null;
        this.errorMessage = '';
        this.status = 'idle';
    }
}

export interface data {
    name: string;
    temperature: string;
    wind: string;
    humidity: string;
}
