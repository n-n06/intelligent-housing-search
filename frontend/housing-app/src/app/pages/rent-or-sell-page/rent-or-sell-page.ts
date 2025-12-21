import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FooterComponent } from '../../common-ui/footer/footer.component';

@Component({
  selector: 'app-rent-or-sell-page',
  imports: [CommonModule, FooterComponent],
  templateUrl: './rent-or-sell-page.html',
  styleUrl: './rent-or-sell-page.css'
})
export class RentOrSellPage {

}
