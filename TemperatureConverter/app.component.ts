import {Component} from '@angular/core';
import {TemperatureConverter} from './temperatureConverter.component';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [TemperatureConverter],
    template: `
        <header class="app-header">
            <h1 class="app-title">Temperature Converter</h1>
        </header>

        <main class="app-content">
            <temperature-converter></temperature-converter>
        </main>
    `,
    styles: [`
        .app-header {
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            height: 72px;
            background: #16181d;
        }

        .app-title {
            margin: 0;
            text-align: center;
            font-size: 26px;
            font-weight: 600;
            color: #3ea55f;
        }

        .app-content {
            display: flex;
            justify-content: center;
        }
    `]
})

export class AppComponent { }
