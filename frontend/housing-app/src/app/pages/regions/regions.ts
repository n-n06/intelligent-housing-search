import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ALMATY_REGIONS } from '../../data/regions';

@Component({
  selector: 'app-regions',
  templateUrl: './regions.html',
  styleUrls: ['./regions.css']
})
export class RegionsComponent {
  regions = ALMATY_REGIONS;

  constructor(private router: Router) {}

  openRegion(regionKey: string) {
    this.router.navigate(['/', regionKey, 'select']);
  }
}
