import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class GeocodeService {

  private urlEndPoint = 'https://app.geocodeapi.io/api/v1';
  private apiKey: any;

  constructor(private http: HttpClient) {
    console.log('Creating Geocode Service');
  }

  setApi(key): void {
    this.apiKey = key;
  }

  getCityGeocode(city): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/search?text=' + city + '&apikey=' + this.apiKey);
  }
}
