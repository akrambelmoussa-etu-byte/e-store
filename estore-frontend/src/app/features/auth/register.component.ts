import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { ToastService } from '../../core/services/toast.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h2 class="section-title mb-4">Créer un compte</h2>

            <form [formGroup]="form" (ngSubmit)="submit()" novalidate>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Prénom</label>
                  <input class="form-control" formControlName="firstName" />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Nom</label>
                  <input class="form-control" formControlName="lastName" />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" formControlName="email" />
                @if (form.controls.email.touched && form.controls.email.invalid) {
                  <small class="text-danger">Email invalide</small>
                }
              </div>

              <div class="mb-3">
                <label class="form-label">Mot de passe (6 caractères min.)</label>
                <input type="password" class="form-control" formControlName="password" />
                @if (form.controls.password.touched && form.controls.password.invalid) {
                  <small class="text-danger">Mot de passe trop court</small>
                }
              </div>

              <button class="btn btn-primary w-100" [disabled]="form.invalid || loading">
                @if (loading) {
                  <span class="spinner-border spinner-border-sm me-2"></span>
                }
                S'inscrire
              </button>
            </form>

            <p class="text-center mt-3 mb-0">
              Déjà inscrit ? <a routerLink="/login">Se connecter</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  `
})
export class RegisterComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);
  private toast = inject(ToastService);

  loading = false;

  form = this.fb.nonNullable.group({
    firstName: ['', [Validators.required]],
    lastName: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]]
  });

  submit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.auth.register(this.form.getRawValue()).subscribe({
      next: () => {
        this.toast.success('Inscription réussie, bienvenue !');
        this.router.navigate(['/']);
      },
      error: () => (this.loading = false),
      complete: () => (this.loading = false)
    });
  }
}
