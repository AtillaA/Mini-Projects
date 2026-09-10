import {Component, OnInit} from '@angular/core';
import {FormsModule} from '@angular/forms';

@Component({
    selector: 'temperature-converter',
    standalone: true,
    imports: [FormsModule],
    templateUrl: './temperatureConverter.component.html',
    styleUrls: ['./temperatureConverter.component.scss']
})

export class TemperatureConverter implements OnInit {
    celcius: number | null = null;
    fahrenheit: number | null = null;
    kelvin: number | null = null;

    // C = (F - 32) x 5/9
    // C = K - 273.15

    // F = C x 9/5 + 32
    // F = (K - 273.15) x 9/5 + 32 

    // K = C + 273.15
    // K = (F - 32) x 5/9 + 273.15

    ngOnInit() {
        this.celcius = null;
        this.fahrenheit = null;
        this.kelvin = null;
    }

    // Celcius
    onCelciusChange(value: number | null): void {
        if (this.isBlank(value)) {
            this.fahrenheit = null;
            this.kelvin = null;
            return;
        }
        
        const celcius = Number(value);
        this.fahrenheit = this.round(celcius * 9 / 5 + 32);
        this.kelvin = this.round(celcius + 273.15);
    }

    // Fahrenheit
    onFahrenheitChange(value: number | null): void {
        if (this.isBlank(value)) {
            this.celcius = null;
            this.kelvin = null;
            return;
        }

        const celcius = (Number(value) - 32) * 5 / 9;
        this.celcius = this.round(celcius);
        this.kelvin = this.round(celcius + 273.15);
    }

    // Kelvin
    onKelvinChange(value: number | null): void {
        if (this.isBlank(value)) {
            this.celcius = null;
            this.fahrenheit = null;
            return;
        }

        const celcius = Number(value) - 273.15;
        this.celcius = this.round(celcius);
        this.fahrenheit = this.round(celcius * 9 / 5 + 32);
    }

    // clear other fields for an emptied input 
    private isBlank(value: number | null): boolean { return value === null || value === undefined || String(value).trim() === '' || isNaN(Number(value)); }

    // display 1 decimal
    private round(value: number): number { return Math.round(value * 10) / 10; }
}
