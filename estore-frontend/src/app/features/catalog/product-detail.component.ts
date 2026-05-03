import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProductService } from '../../core/services/product.service';
import { CartService } from '../../core/services/cart.service';
import { ReviewService } from '../../core/services/review.service';
import { AuthService } from '../../core/services/auth.service';
import { ToastService } from '../../core/services/toast.service';
import { Product } from '../../core/models/product.model';
import { Review } from '../../core/models/review.model';
import { LoaderComponent } from '../../shared/components/loader.component';
import { ReviewFormComponent } from '../reviews/review-form.component';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LoaderComponent, ReviewFormComponent],
  template: `
    @if (loading) {
      <app-loader />
    } @else if (product) {
      <a routerLink="/" class="text-decoration-none mb-3 d-inline-block">&larr; Retour au catalogue</a>

      <div class="row g-4">
        <div class="col-md-5">
          <img [src]="product.imageUrl || 'https://placehold.co/600x400'" class="img-fluid rounded shadow-sm" [alt]="product.name" />
        </div>
        <div class="col-md-7">
          <h2>{{ product.name }}</h2>
          <span class="badge bg-secondary mb-3">{{ product.categoryName }}</span>
          <p class="text-muted">{{ product.description }}</p>
          <h3 class="text-primary my-3">{{ product.price | number:'1.2-2' }} MAD</h3>
          <p>
            <span class="badge bg-{{ product.stock > 0 ? 'success' : 'danger' }}">
              {{ product.stock > 0 ? product.stock + ' unités en stock' : 'Rupture de stock' }}
            </span>
          </p>

          <div class="d-flex align-items-center gap-3 mt-4">
            <input
              type="number"
              min="1"
              [max]="product.stock"
              [(ngModel)]="quantity"
              class="form-control"
              style="width: 100px"
            />
            <button class="btn btn-primary" [disabled]="product.stock < 1 || adding" (click)="addToCart()">
              @if (adding) {
                <span class="spinner-border spinner-border-sm me-2"></span>
              }
              Ajouter au panier
            </button>
          </div>
        </div>
      </div>

      <hr class="my-5" />

      <h4 class="section-title mb-4">Avis clients ({{ reviews.length }})</h4>

      @if (auth.isAuthenticated) {
        <app-review-form [productId]="product.id" (created)="loadReviews()" />
      } @else {
        <div class="alert alert-info">
          <a routerLink="/login">Connectez-vous</a> pour déposer un avis.
        </div>
      }

      @if (reviews.length === 0) {
        <p class="text-muted">Aucun avis pour ce produit pour le moment.</p>
      } @else {
        <div class="list-group mt-3">
          @for (r of reviews; track r.id) {
            <div class="list-group-item">
              <div class="d-flex justify-content-between">
                <strong>{{ r.authorName }}</strong>
                <small class="text-muted">{{ r.createdAt | date:'short' }}</small>
              </div>
              <div class="star-rating">
                @for (s of stars(r.rating); track $index) { <span>★</span> }
                @for (s of stars(5 - r.rating); track $index) { <span class="text-secondary">☆</span> }
              </div>
              <p class="mb-0 mt-1">{{ r.comment }}</p>
            </div>
          }
        </div>
      }
    }
  `
})
export class ProductDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private productSvc = inject(ProductService);
  private cartSvc = inject(CartService);
  private reviewSvc = inject(ReviewService);
  private toast = inject(ToastService);
  auth = inject(AuthService);

  product: Product | null = null;
  reviews: Review[] = [];
  quantity = 1;
  loading = true;
  adding = false;

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) return;
    this.productSvc.getById(id).subscribe({
      next: (r) => {
        this.product = r.data ?? null;
        this.loading = false;
        this.loadReviews();
      },
      error: () => (this.loading = false)
    });
  }

  loadReviews(): void {
    if (!this.product) return;
    this.reviewSvc.byProduct(this.product.id).subscribe({
      next: (r) => (this.reviews = r.data ?? []),
      error: () => (this.reviews = [])
    });
  }

  addToCart(): void {
    if (!this.product) return;
    if (!this.auth.isAuthenticated) {
      this.toast.info('Veuillez vous connecter pour ajouter au panier');
      this.router.navigate(['/login']);
      return;
    }
    this.adding = true;
    this.cartSvc.add(this.product.id, this.quantity).subscribe({
      next: () => {
        this.toast.success('Ajouté au panier');
        this.adding = false;
      },
      error: () => (this.adding = false)
    });
  }

  stars(n: number): number[] {
    return Array.from({ length: n });
  }
}
