import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApartmentsService } from '../../services/apartments.service';
import { Apartment } from '../../models/apartment.model';

@Component({
  standalone: true,
  selector: 'app-apartments',
  templateUrl: './apartments.component.html',
  styleUrl: './apartments.component.css',
  imports: [CommonModule] // ← ВАЖНО
})
export class ApartmentsComponent {
  apartments: Apartment[] = [];

  constructor(private apartmentsService: ApartmentsService) {
    this.apartmentsService.getApartments()
      .subscribe(data => this.apartments = data);
  }
}
