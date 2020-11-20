import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {WeatherComponent} from './weather/weather.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {HistoricComponent} from './historic/historic.component';
import {SensorsComponent} from './sensors/sensors.component';


const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'sensors', component: SensorsComponent },
  { path: 'weather', component: WeatherComponent },
  { path: 'historic', component: HistoricComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
