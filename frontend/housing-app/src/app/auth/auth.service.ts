import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { tap } from 'rxjs';
import { TokenResponse, UserLogin, UserRegistration } from './auth.interface';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  http : HttpClient = inject(HttpClient);
  router : Router = inject(Router);
  cookie : CookieService = inject(CookieService);

  apiUrl : string = 'http://127.0.0.1:8000/auth/'
  accessToken : string | null = '';
  refreshToken : string | null= ''; //it should redirect us back to the login page after rega

  registered : boolean = false;

  isRegistered() : boolean {
    return this.registered;
  }

  isAuthenticated() : boolean {
    if (!this.accessToken) {
      this.accessToken = this.cookie.get('accessToken');
      this.refreshToken = this.cookie.get('refreshToken');
    }
    return !!this.accessToken;
  }

  register(payload: UserRegistration) {
    return this.http.post(
      `${this.apiUrl}register/`,
      payload,
      {
        headers: { 'Content-Type': 'application/json' }
      }
    ).pipe(
      tap(() => this.registered = true)
    );
  }

  login(payload: UserLogin) {
    const body = new URLSearchParams();
    body.set('username', payload.username);
    body.set('password', payload.password);

    return this.http.post<TokenResponse>(
      `${this.apiUrl}login/`,
      body.toString(),
      {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }
    ).pipe(
      tap(res => {
        this.saveTokens(res);
      })
    );
  }



  logout() {
    this.http.post(`${this.apiUrl}logout/`, {
      refresh: this.refreshToken
    });

    this.cookie.deleteAll();
    this.accessToken = null;
    this.refreshToken = null;
    this.router.navigate(['/login']);
  }

  saveTokens(res: TokenResponse) {
    this.accessToken = res.access;
    this.refreshToken = res.refresh;

    this.cookie.set('accessToken', this.accessToken);
    this.cookie.set('refreshToken', this.refreshToken);
  }

}
