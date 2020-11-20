import { Component, OnInit } from '@angular/core';
import {BackendService} from '../backend.service';

@Component({
  selector: 'app-home-current',
  templateUrl: './home-current.component.html',
  styleUrls: ['./home-current.component.css']
})
export class HomeCurrentComponent implements OnInit {

  homeReport: any;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getHome().subscribe(json => {
      this.parseHome(json);
    });
    this.backend.ioSocket.on('homeData', json => this.parseHome(JSON.parse(json)));
  }

  parseHome(json): void {
      this.homeReport = json;
      console.log(json);
  }
}
