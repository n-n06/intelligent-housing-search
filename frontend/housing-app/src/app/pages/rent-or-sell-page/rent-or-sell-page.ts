import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FooterComponent } from '../../common-ui/footer/footer.component';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-rent-or-sell-page',
  imports: [CommonModule, FooterComponent],
  templateUrl: './rent-or-sell-page.html',
  styleUrl: './rent-or-sell-page.css'
})
export class RentOrSellPage {
  private router : Router = inject(Router);
  private route: ActivatedRoute = inject(ActivatedRoute);

  region!: string;

  ngOnInit() {
    this.region = this.route.snapshot.paramMap.get('region')!;
  }

  redirectToType(type: 'rent' | 'sell') {
    this.router.navigate(['/', this.region, type]);
  }

}
