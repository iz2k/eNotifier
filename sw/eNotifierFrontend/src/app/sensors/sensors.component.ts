import { Component, OnInit } from '@angular/core';
import {BackendService} from '../backend.service';

@Component({
  selector: 'app-sensors',
  templateUrl: './sensors.component.html',
  styleUrls: ['./sensors.component.css']
})
export class SensorsComponent implements OnInit {

  storedBaselineEco2: any;
  storedBaselineTvoc: any;
  currentBaselineEco2: any;
  currentBaselineTvoc: any;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getWeatherConfig().subscribe(json => {
      this.parseWeatherConfig(json);
    });
    this.backend.ioSocket.on('homeData', json => this.parseHome(JSON.parse(json)));
  }

  parseWeatherConfig(json): void {
    this.storedBaselineEco2 = json.baselineEco2;
    this.storedBaselineTvoc = json.baselineTvoc;
  }

  private parseHome(json): void {
    console.log(json);
    this.currentBaselineEco2 = json.baseline[0];
    this.currentBaselineTvoc = json.baseline[1];
  }

  triggerCalibration(): void {
    this.backend.resetBaseline().subscribe();
  }

  saveBaselines(): void {
    this.backend.setWeatherParameters(
      [
        {parameter: 'baselineEco2', value: this.currentBaselineEco2},
        {parameter: 'baselineTvoc', value: this.currentBaselineTvoc},
      ]).subscribe(json =>
    {
      this.parseWeatherConfig(json);
      this.backend.reloadSensors().subscribe();
    });
  }
}
