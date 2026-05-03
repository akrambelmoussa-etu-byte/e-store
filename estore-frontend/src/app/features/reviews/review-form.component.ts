import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ReviewService } from '../../core/services/review.service';
import { ToastService } from '../../core/services/toast.service';

@Component({
  selector: 'app-review-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <h6 class="mb-3">Donnez votre avis</h6>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <div class="mb-3">
            <label class="form-label me-3">Note</label>
            <span class="star-rating cursor-pointer">
              @for (n of [1,2,3,4,5]; track n) {
                <span (click)="setRating(n)" [class.text-secondary]="form.controls.rating.value < n">★</span>
              }
            </span>
          </div>
          <div class="mb-3">
            <textarea class="form-control" rows="3" formControlName="comment" placeholder="Votre commentaire"></textarea>
          </div>
          <button class="btn btn-primary btn-sm" [disabled]="form.invalid || sending">
            @if (sending) { <span class="spinner-border spinner-border-sm me-2"></span> }
            Publier
          </button>
        </form>
      </div>
    </div>
  `
})
export class ReviewFormComponent {
  @Input({ required: true }) productId!: number;
  @Output() created = new EventEmitter<void>();

  private fb = inject(FormBuilder);
  private reviewSvc = inject(ReviewService);
  private toast = inject(ToastService);

  sending = false;

  form = this.fb.nonNullable.group({
    rating: [5, [Validators.required, Validators.min(1), Validators.max(5)]],
    comment: ['', [Validators.required, Validators.maxLength(1000)]]
  });

  setRating(n: number): void {
    this.form.controls.rating.setValue(n);
  }

  submit(): void {
    if (this.form.invalid) return;
    this.sending = true;
    const { rating, comment } = this.form.getRawValue();
    this.reviewSvc.create({ productId: this.productId, rating, comment }).subscribe({
      next: () => {
        this.toast.success('Avis publié, merci !');
        this.form.reset({ rating: 5, comment: '' });
        this.created.emit();
        this.sending = false;
      },
      error: () => (this.sending = false)
    });
  }
}
