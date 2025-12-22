import { Component, inject } from '@angular/core';
import { Button } from '../../common-ui/button/button';
import { Router } from '@angular/router';
import { HeaderComponent } from '../../common-ui/header/header.component';
import { FooterComponent } from '../../common-ui/footer/footer.component';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-home-page',
  imports: [FooterComponent],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css'
})
export class HomePage {
  router: Router = inject(Router);
  authService: AuthService = inject(AuthService);

  redirectToLogin() {
    this.router.navigate(['/login']);
  }

  redirectToRegister() {
    this.router.navigate(['/register']);
  }

  redirectToRegions() {
    this.router.navigate(['/regions'])
  }

  isAuthenticated() {
    return this.authService.isAuthenticated();
  }
}
