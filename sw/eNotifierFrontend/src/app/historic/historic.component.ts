import {Component, OnInit, QueryList, ViewChildren} from '@angular/core';
import {BackendService} from '../backend.service';
import {FormControl} from '@angular/forms';
import {ChartDataSets} from 'chart.js';
import {BaseChartDirective, Color} from 'ng2-charts';

@Component({
  selector: 'app-historic',
  templateUrl: './historic.component.html',
  styleUrls: ['./historic.component.css']
})
export class HistoricComponent implements OnInit {

  constructor(private backend: BackendService) { }

  date: FormControl;
  dateStart = new Date();
  dateStop = new Date();
  historicData = [];
  viewToggle = 'table';

  @ViewChildren( BaseChartDirective) charts: QueryList<BaseChartDirective>;
  ChartDataHome: ChartDataSets[] = [];
  ChartDataCity: ChartDataSets[] = [];
  ChartOptions = this.chartOptionsY1Y2vsX('time', 'Date', 'linear', '', 'linear', '');

  ChartPlugins = {};
  ChartColors: Color[] = [
    {
      borderColor: 'black',
      backgroundColor: 'rgba(255,255,0,0.28)',
    },
  ];

  ChartLegendTrue = true;
  ChartTypeLine = 'line';

  pluginzoom = {
      zoom: {
        pan: {
          enabled: true,
          mode: 'xy',
        },
        zoom: {
          enabled: true,
          mode: 'xy',
        },
      }
  };

  chartOptionsY1Y2vsX(xtype, xlabel, y1type, y1label, y2type, y2label): any
  {
    const myChartOptions =  {
      responsive: true,
      scales: {
        xAxes: [{
          type: xtype,
          scaleLabel: {
            display: true,
            labelString: xlabel
          }
        }],
      yAxes: [{
        type: y1type,
        position: 'left',
        id: 'y-axis-1',
        scaleLabel: {
          display: true,
          labelString: y1label
        }
      },
      {
        type: y2type,
        id: 'y-axis-2',
        position: 'right',
        scaleLabel: {
          display: true,
          labelString: y2label
        }
      }]
    },
      plugins: {}
    };
    return myChartOptions;
  }


  ngOnInit(): void {
    this.date = new FormControl(new Date());
    this.dateStart.setMonth(this.dateStart.getMonth() - 1);
    this.updateData();
  }

  updateData(): void {
    const filter = {
      startDate: this.dateStart,
      stopDate: this.dateStop
    };
    this.backend.getMeasurements(filter).subscribe(json => {
      this.historicData = json;
      console.log(json);
      this.updateChartDataHome();
      this.updateChartDataCity();
      this.ChartOptions.plugins = this.pluginzoom;
    });
  }

  private updateChartDataHome(): void {
    let i;
    const dataTemperature = [];
    const dataHumidity = [];
    const dataPressure = [];
    const dataEco2 = [];
    const dataTvoc = [];
    for (i = 0; i < this.historicData.length; i++) {
      const temperature = {x: this.historicData[i]['datetime'], y: this.historicData[i]['homeMeas']['temperature']};
      dataTemperature.push(temperature);
      const humidity = {x: this.historicData[i]['datetime'], y: this.historicData[i]['homeMeas']['humidity']};
      dataHumidity.push(humidity);
      const pressure = {x: this.historicData[i]['datetime'], y: this.historicData[i]['homeMeas']['pressure']};
      dataPressure.push(pressure);
      const eco2 = {x: this.historicData[i]['datetime'], y: this.historicData[i]['homeMeas']['eco2']};
      dataEco2.push(eco2);
      const tvoc = {x: this.historicData[i]['datetime'], y: this.historicData[i]['homeMeas']['tvoc']};
      dataTvoc.push(tvoc);
    }

    this.ChartDataHome = [
        { data: dataTemperature, label: 'Temperature [ºC]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-1'},
        { data: dataHumidity, label: 'Humidity [%]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-1'},
        { data: dataPressure, label: 'Pressure [mb]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-2'},
        { data: dataEco2, label: 'eCO2 [ppm]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-2'},
        { data: dataTvoc, label: 'TVOC [ppb]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-2'}
      ];

  }

  private updateChartDataCity(): void {
    let i;
    const dataTemperature = [];
    const dataHumidity = [];
    const dataPressure = [];
    const dataUvi = [];
    const dataWind = [];
    const dataPop = [];
    for (i = 0; i < this.historicData.length; i++) {
      const temperature = {x: this.historicData[i]['datetime'], y: this.historicData[i]['cityMeas']['temperature']};
      dataTemperature.push(temperature);
      const humidity = {x: this.historicData[i]['datetime'], y: this.historicData[i]['cityMeas']['humidity']};
      dataHumidity.push(humidity);
      const pressure = {x: this.historicData[i]['datetime'], y: this.historicData[i]['cityMeas']['pressure']};
      dataPressure.push(pressure);
      const uvi = {x: this.historicData[i]['datetime'], y: this.historicData[i]['cityMeas']['uvi']};
      dataUvi.push(uvi);
      const wind = {x: this.historicData[i]['datetime'], y: (this.historicData[i]['cityMeas']['wind_speed']*3.6).toFixed(0)};
      dataWind.push(wind);
      const pop = {x: this.historicData[i]['datetime'], y: (this.historicData[i]['cityMeas']['pop']*100).toFixed(0)};
      dataPop.push(pop);
    }

    this.ChartDataCity = [
        { data: dataTemperature, label: 'Temperature [ºC]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-1'},
        { data: dataHumidity, label: 'Humidity [%]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-1'},
        { data: dataPressure, label: 'Pressure [mb]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-2'},
        { data: dataUvi, label: 'UV [uvi]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-1'},
        { data: dataWind, label: 'Wind [km/h]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-1'},
        { data: dataPop, label: 'POP [%]', pointRadius: 0,  cubicInterpolationMode: 'monotone', yAxisID: 'y-axis-1'}
      ];
  }

  resetZoom(id): void{
    const arrayResult = this.charts.toArray();
    // @ts-ignore
    arrayResult[id].chart.resetZoom();
  }
}
