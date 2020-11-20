import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { WeatherComponent } from './weather/weather.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import {SocketIoModule} from 'ngx-socket-io';
import {BackendService} from './backend.service';
import {HttpClientModule} from '@angular/common/http';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatInputModule } from '@angular/material/input';
import {JSBAngularFlipClockModule} from 'jsb-angular-flip-clock';
import {MatNativeDateModule} from '@angular/material/core';
import {MomentTimezonePickerModule} from 'moment-timezone-picker';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatSelectModule} from '@angular/material/select';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import { WeatherCurrentComponent } from './weather/weather-current/weather-current.component';
import { HomeCurrentComponent } from './home-current/home-current.component';
import { HistoricComponent } from './historic/historic.component';
import {MatButtonToggleModule} from '@angular/material/button-toggle';
import {ChartsModule} from 'ng2-charts';
import 'hammerjs';
import 'chartjs-plugin-zoom';
import { SensorsComponent } from './sensors/sensors.component';


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    WeatherComponent,
    DashboardComponent,
    WeatherCurrentComponent,
    HomeCurrentComponent,
    HistoricComponent,
    SensorsComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    JSBAngularFlipClockModule,
    NgbModule,
    SocketIoModule,
    HttpClientModule,
    MatFormFieldModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatSelectModule,
    MatButtonModule,
    MatCheckboxModule,
    MatSlideToggleModule,
    MatIconModule,
    MatButtonToggleModule,
    ReactiveFormsModule,
    MomentTimezonePickerModule,
    FormsModule,
    ChartsModule
  ],
  providers: [BackendService],
  bootstrap: [AppComponent]
})
export class AppModule { }
