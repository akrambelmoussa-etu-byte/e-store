import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { CartService } from '../../core/services/cart.service';
import { ToastService } from '../../core/services/toast.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h2 class="section-title mb-4">Connexion</h2>

            <form [formGroup]="form" (ngSubmit)="submit()" novalidate>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" formControlName="email" placeholder="vous@exemple.ma" />
                @if (form.controls.email.touched && form.controls.email.invalid) {
                  <small class="text-danger">Email invalide</small>
                }
              </div>

              <div class="mb-3">
                <label class="form-label">Mot de passe</label>
                <input type="password" class="form-control" formControlName="password" />
                @if (form.controls.password.touched && form.controls.password.invalid) {
                  <small class="text-danger">Mot de passe requis</small>
                }
              </div>

              <button class="btn btn-primary w-100" [disabled]="form.invalid || loading">
                @if (loading) {
                  <span class="spinner-border spinner-border-sm me-2"></span>
                }
                Se connecter
              </button>
            </form>

            <p class="text-center mt-3 mb-0">
              Pas encore inscrit ? <a routerLink="/register">Créer un compte</a>
            </p>

            <div class="alert alert-info mt-3 small mb-0">
              <strong>Comptes de test :</strong><br />
              admin&#64;estore.ma / Admin&#64;123<br />
              user&#64;estore.ma / User&#64;123
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);
  private toast = inject(ToastService);
  private cartSvc = inject(CartService);

  loading = false;

  form = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]]
  });

  submit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    const { email, password } = this.form.getRawValue();
    this.auth.login(email, password).subscribe({
      next: () => {
        this.toast.success('Connexion réussie');
        this.cartSvc.get().subscribe();
        this.router.navigate(['/']);
      },
      error: () => (this.loading = false),
      complete: () => (this.loading = false)
    });
  }
}
