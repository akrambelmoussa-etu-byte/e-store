import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { UserService } from '../../core/services/user.service';
import { ToastService } from '../../core/services/toast.service';
import { LoaderComponent } from '../../shared/components/loader.component';
import { UserDetails } from '../../core/models/user.model';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, LoaderComponent],
  template: `
    <h2 class="section-title mb-4">Mon profil</h2>

    @if (loading) {
      <app-loader />
    } @else {
      <div class="card shadow-sm">
        <div class="card-body p-4">
          <form [formGroup]="form" (ngSubmit)="save()">
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
              <label class="form-label">Email (non modifiable)</label>
              <input class="form-control" [value]="me?.user?.email" disabled />
            </div>

            <h5 class="mt-4 mb-3">Adresse</h5>

            <div formGroupName="profile">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Téléphone</label>
                  <input class="form-control" formControlName="phone" />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Ville</label>
                  <input class="form-control" formControlName="city" />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Adresse</label>
                <input class="form-control" formControlName="address" />
              </div>

              <div class="mb-3">
                <label class="form-label">Pays</label>
                <input class="form-control" formControlName="country" />
              </div>
            </div>

            <button class="btn btn-primary" [disabled]="saving">
              @if (saving) {
                <span class="spinner-border spinner-border-sm me-2"></span>
              }
              Enregistrer
            </button>
          </form>
        </div>
      </div>
    }
  `
})
export class ProfileComponent implements OnInit {
  private fb = inject(FormBuilder);
  private userSvc = inject(UserService);
  private toast = inject(ToastService);

  loading = true;
  saving = false;
  me: UserDetails | null = null;

  form = this.fb.nonNullable.group({
    firstName: ['', Validators.required],
    lastName: ['', Validators.required],
    profile: this.fb.nonNullable.group({
      phone: [''],
      address: [''],
      city: [''],
      country: ['']
    })
  });

  ngOnInit(): void {
    this.userSvc.me().subscribe({
      next: (r) => {
        this.me = r.data ?? null;
        if (this.me) {
          this.form.patchValue({
            firstName: this.me.user.firstName,
            lastName: this.me.user.lastName,
            profile: {
              phone: this.me.profile?.phone ?? '',
              address: this.me.profile?.address ?? '',
              city: this.me.profile?.city ?? '',
              country: this.me.profile?.country ?? ''
            }
          });
        }
        this.loading = false;
      },
      error: () => (this.loading = false)
    });
  }

  save(): void {
    if (this.form.invalid) return;
    this.saving = true;
    this.userSvc.updateMe(this.form.getRawValue()).subscribe({
      next: () => {
        this.toast.success('Profil mis à jour');
        this.saving = false;
      },
      error: () => (this.saving = false)
    });
  }
}
