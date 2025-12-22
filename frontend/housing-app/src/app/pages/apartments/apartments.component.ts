import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApartmentsService } from '../../services/apartments.service';
import { Apartment } from '../../models/apartment.model';
import { ActivatedRoute } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-apartments',
  templateUrl: './apartments.component.html',
  styleUrl: './apartments.component.css',
  imports: [CommonModule] 
})
export class ApartmentsComponent {
  apartments: Apartment[] = [];
  region!: string;
  listingType!: 'rent' | 'sell';

  constructor(
    private route: ActivatedRoute,
    private apartmentsService: ApartmentsService
  ) {}

  ngOnInit() {
    this.region = this.route.snapshot.paramMap.get('region')!;
    this.listingType = this.route.snapshot.data['type'];

    this.apartmentsService
      .getApartments(this.region, this.listingType)
      .subscribe(data => (this.apartments = data));
  }
}
