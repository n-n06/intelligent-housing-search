import { Component, inject } from '@angular/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-registration-page',
  imports: [
    FormsModule,
    ReactiveFormsModule
  ],
  templateUrl: './registration-page.html',
  styleUrl: './registration-page.css'
})
export class RegistrationPage {
  // message = '';
  submitted = false;

  authService: AuthService = inject(AuthService);
  router : Router = inject(Router);

  form = new FormGroup({
    email: new FormControl<string | null>(null, Validators.required),
    first_name: new FormControl<string | null>(null, Validators.required),
    last_name: new FormControl<string | null>(null, Validators.required),
    password : new FormControl<string | null>(null, Validators.required),
    confirm_password: new FormControl<string | null>(null, Validators.required)
  });


  registrationSuccess: boolean = false;

  successMessage: string = '';
  errorMessages: string[] = [];

  isLoading: boolean = false;

  onSubmit() {
    this.isLoading = true;

    const password = this.form.get('password')?.value;
    const confirmPassword = this.form.get('confirm_password')?.value;

    if (password !== confirmPassword) {
      this.isLoading = false;
      this.errorMessages = ['Passwords do not match.'];
      return;
    }

    if (this.form.valid) {
      this.submitted = true;
      this.registrationSuccess = false;
      this.errorMessages = [];
      this.successMessage = '';

      let payload = {
        ...this.form.value,
        role: 'customer'
      };


      //@ts-ignore
      this.authService.register(payload).subscribe({
        next: (res: any) => {
          this.isLoading = false;
          this.registrationSuccess = true;
          this.successMessage = 'Registration successful! Redirecting to login page...';
          setTimeout(() => this.router.navigate(['/login']), 2000);
        },
        error: (err: any) => {
          this.isLoading = false;
          if (err.error) {
              const errorMessage = err.error.detail[0].msg;
              this.errorMessages.push(errorMessage.charAt(0).toUpperCase() + errorMessage.slice(1));
          } else {
            this.errorMessages.push('Registration failed. Please try again.');
          }
        }
      });
    } else {
      this.isLoading = false;
    }
  }
}
