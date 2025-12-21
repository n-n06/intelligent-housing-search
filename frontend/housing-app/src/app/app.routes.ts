import { Routes } from '@angular/router';
import { HeaderComponent } from './common-ui/header/header.component';
import { LoginPage } from './pages/login-page/login-page';
import { RegistrationPage } from './pages/registration-page/registration-page';
import { canActivateAuth } from './auth/access.guard';
import { HomePage } from './pages/home-page/home-page';
import { PageNotFound } from './pages/page-not-found/page-not-found';
import { ApartmentsComponent } from './pages/apartments/apartments.component';
import { RentOrSellPage } from './pages/rent-or-sell-page/rent-or-sell-page';

export const routes: Routes = [
    {
        path: '',
        component: HeaderComponent,
        children: [
            {
                path: '',
                component: HomePage,
            },
            {
                path: 'login',
                component: LoginPage
            },
            {
                path: 'select',
                component: RentOrSellPage,
                canActivate: [canActivateAuth]
            },
            {
                path: 'register',
                component: RegistrationPage
            },
            {
                path: 'apartments',
                component: ApartmentsComponent,
                canActivate: [canActivateAuth]
            },
            {
                path: '**',
                component: PageNotFound
            }
        ]
    },
];
