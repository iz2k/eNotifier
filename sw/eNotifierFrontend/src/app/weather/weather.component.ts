import {Component, OnInit, ViewChild} from '@angular/core';
import {BackendService} from '../backend.service';
import {GeocodeService} from './geocode.service';

import Map from 'ol/Map';
import View from 'ol/View';
import OSM from 'ol/source/OSM';
import * as olProj from 'ol/proj';
import TileLayer from 'ol/layer/Tile';
import {WeatherCurrentComponent} from './weather-current/weather-current.component';

@Component({
  selector: 'app-weather',
  templateUrl: './weather.component.html',
  styleUrls: ['./weather.component.css']
})
export class WeatherComponent implements OnInit {

  cityName = '';
  cityAlias: any;
  geocodeAPI: any;
  geocodeResult: any;
  configCityName: any;
  configCityAlias: any;
  configGeocodeAPI: any;
  location: any;
  map: any;

  @ViewChild(WeatherCurrentComponent)
  private weatherCurrent: WeatherCurrentComponent;

  constructor(private backend: BackendService, private geocode: GeocodeService) { }

  ngOnInit(): void {
    this.backend.getWeatherConfig().subscribe(json => {
      this.parseWeatherConfig(json);
      this.map = new Map({
      controls: [],
      target: 'cityMap',
      layers: [
        new TileLayer({
          source: new OSM()
        })
      ],
      view: new View({
        center: olProj.fromLonLat([0, 0]),
        zoom: 1
      })
    });
    });
  }

  parseWeatherConfig(json): void {
    this.geocodeAPI = json.geocodeApi;
    this.configGeocodeAPI = this.geocodeAPI;
    this.geocode.setApi(this.geocodeAPI);
    this.cityName = json.location;
    this.cityAlias = json.cityAlias;
    this.configCityName = this.cityName;
    this.configCityAlias = this.cityAlias;
    this.searchCity();
  }

  searchCity(): void {
    this.geocode.getCityGeocode(this.cityName).subscribe(json => {
      this.geocodeResult = json;
      console.log('Geocode result:');
      console.log(this.geocodeResult);
      if (this.geocodeResult.features[0] !== undefined)
      {
        this.location = this.geocodeResult.features[0];
        this.map.setView(new View({
          center: olProj.fromLonLat(this.location.geometry.coordinates),
          zoom: 13
        }));
      }else
      {
        this.location = undefined;
        this.map.setView(new View({
          center: olProj.fromLonLat([0, 0]),
          zoom: 1
        }));
      }
      console.log(this.location);
    });
  }

  saveLocation(): void {
    this.backend.setWeatherParameters(
      [
        {parameter: 'location', value: this.location.properties.name},
        {parameter: 'longitude', value: this.location.geometry.coordinates[0]},
        {parameter: 'latitude', value: this.location.geometry.coordinates[1]}
      ]).subscribe(json =>
    {
      this.parseWeatherConfig(json);
      this.weatherCurrent.ngOnInit();
    });
  }

  saveGeocodeApi(): void {
    this.backend.setWeatherParameters(
      [
        {parameter: 'geocodeApi', value: this.geocodeAPI}
      ]).subscribe(json =>
    {
      this.parseWeatherConfig(json);
    });
  }

  saveAlias(): void {
    this.backend.setWeatherParameters(
      [
        {parameter: 'cityAlias', value: this.cityAlias}
      ]).subscribe(json =>
    {
      this.parseWeatherConfig(json);
    });
  }
}
