import { Component } from '@angular/core';

import { data } from './weatherDetails.component';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})

export class AppComponent {
    /**
     * Weather records start empty and filled by live WeatherAPI responses
     * <weather-details> fetches a record - stores it - passes back as an array as input 
     * Component is both the data source and the cache that keeps repeat searches off
     */
    weatherData: data[] = [];

    /** adds a freshly fetched record - replacing any earlier entry */
    addRecord(record: data) {
        const index = this.weatherData.findIndex(
            (existing) => existing.name.toLowerCase() === record.name.toLowerCase()
        );

        if (index === -1) {
            this.weatherData = [...this.weatherData, record];
        } else {
            const next = [...this.weatherData];
            next[index] = record;
            this.weatherData = next;
        }
    }
}
