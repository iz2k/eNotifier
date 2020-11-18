import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-weather-current',
  templateUrl: './weather-current.component.html',
  styleUrls: ['./weather-current.component.css']
})
export class WeatherCurrentComponent implements OnInit {

  weatherReport: any;
  weatherIconUrl: any;

  constructor(private backend: BackendService,) { }

  ngOnInit(): void {
    this.backend.getWeather().subscribe(json => {
      this.parseWeather(json);
    });
  }

  parseWeather(json): void {
      this.weatherReport = json;
      this.weatherIconUrl = 'http://openweathermap.org/img/wn/' + this.weatherReport.current.weather[0].icon + '@4x.png';
      console.log(json);
  }
}
