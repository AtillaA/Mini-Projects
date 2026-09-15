import { Injectable } from '@angular/core';

import { environment } from './environment';
import { CityValidatorService } from './cityValidator.service';
import type { data } from './weatherDetails.component';

interface CacheEntry {
    record: data;
    /** Epoch milliseconds of fetch from WeatherAPI */
    fetchedAt: number;
}

/**
 * to ensure same city is fetched at most once an hour
 * entries are held in memory and mirrored into localStorage - cache survives a page reload
 */
@Injectable({ providedIn: 'root' })
export class WeatherCacheService {
    private static readonly STORAGE_KEY = 'weather-component.cache.v1';

    private readonly entries = new Map<string, CacheEntry>();

    constructor() {
        this.restore();
    }

    /**
     * stored record for `city` or null when nothing is cached or the stored
     * lookup is case- and accent-insensitive
     */
    get(city: string): data | null {
        const key = CityValidatorService.normalise(city);
        const entry = this.entries.get(key);

        if (!entry) {
            return null;
        }

        if (this.isExpired(entry)) {
            this.entries.delete(key);
            this.persist();
            return null;
        }

        return entry.record;
    }

    /**
     * stores a fresh fetch 
     * filed both under the typed text & canonical WeatherAPI name returned
     */
    set(typedTerm: string, record: data): void {
        const entry: CacheEntry = { record, fetchedAt: Date.now() };

        for (const alias of [typedTerm, record.name]) {
            const key = CityValidatorService.normalise(alias);
            if (key) {
                this.entries.set(key, entry);
            }
        }

        this.persist();
    }

    /** every record currently cached and still fresh */
    freshRecords(): data[] {
        const seen = new Set<string>();
        const records: data[] = [];

        for (const entry of this.entries.values()) {
            if (this.isExpired(entry)) {
                continue;
            }
            const key = CityValidatorService.normalise(entry.record.name);
            if (!seen.has(key)) {
                seen.add(key);
                records.push(entry.record);
            }
        }

        return records;
    }

    /** drops everything - in memory and on disk */
    clear(): void {
        this.entries.clear();
        this.persist();
    }

    private isExpired(entry: CacheEntry): boolean {
        return Date.now() - entry.fetchedAt > environment.cacheTtlMs;
    }

    /** loads the cache written by a previous visit - discarding stale entries */
    private restore(): void {
        let raw: string | null = null;

        // reading localStorage throws outright in some privacy modes
        // every access has to be defensive - a broken cache must never break the app
        try {
            raw = localStorage.getItem(WeatherCacheService.STORAGE_KEY);
        } catch {
            return;
        }

        if (!raw) {
            return;
        }

        try {
            const parsed = JSON.parse(raw) as Record<string, CacheEntry>;
            for (const [key, entry] of Object.entries(parsed || {})) {
                if (this.isValidEntry(entry) && !this.isExpired(entry)) {
                    this.entries.set(key, entry);
                }
            }
        } catch {
            // corrupt or hand-edited payload - start from an empty cache.
            this.entries.clear();
        }
    }

    private persist(): void {
        try {
            localStorage.setItem(
                WeatherCacheService.STORAGE_KEY,
                JSON.stringify(Object.fromEntries(this.entries))
            );
        } catch {
            // storage full or unavailable; the in-memory cache still works
        }
    }

    private isValidEntry(entry: CacheEntry): boolean {
        return (
            !!entry &&
            typeof entry.fetchedAt === 'number' &&
            !!entry.record &&
            typeof entry.record.name === 'string' &&
            typeof entry.record.temperature === 'string' &&
            typeof entry.record.wind === 'string' &&
            typeof entry.record.humidity === 'string'
        );
    }
}
