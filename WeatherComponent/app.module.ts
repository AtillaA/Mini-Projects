import { NgModule } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { WeatherDetails } from './weatherDetails.component';

@NgModule({
  declarations: [AppComponent, WeatherDetails],
  imports: [BrowserModule],
  providers: [provideHttpClient()],
  bootstrap: [AppComponent]
})

export class AppModule {}
