import { Component, inject } from '@angular/core';
import { Button } from '../../common-ui/button/button';
import { Router } from '@angular/router';
import { HeaderComponent } from '../../common-ui/header/header.component';
import { FooterComponent } from '../../common-ui/footer/footer.component';

@Component({
  selector: 'app-home-page',
  imports: [Button, HeaderComponent, FooterComponent],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css'
})
export class HomePage {
  router: Router = inject(Router);

  redirectToLogin() {
    this.router.navigate(['/login']);
  }

  redirectToRegister() {
    this.router.navigate(['/register']);
  }
}
