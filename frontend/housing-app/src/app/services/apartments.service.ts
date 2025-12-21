import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Apartment } from '../models/apartment.model';

@Injectable({ providedIn: 'root' })
export class ApartmentsService {
  private url = 'objects.json';
  // потом просто поменяешь на:
  // private url = 'https://api.example.com/apartments';

  constructor(private http: HttpClient) {}

  getApartments(): Observable<Apartment[]> {
    return this.http.get<Apartment[]>(this.url);
  }
}
