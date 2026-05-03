import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ProductService } from '../../core/services/product.service';
import { Category, Product } from '../../core/models/product.model';
import { LoaderComponent } from '../../shared/components/loader.component';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LoaderComponent],
  template: `
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
      <h2 class="section-title mb-0">Notre catalogue</h2>
      <div class="d-flex gap-2 flex-wrap mt-2 mt-md-0">
        <input
          type="text"
          class="form-control"
          style="width: 220px"
          placeholder="Rechercher..."
          [(ngModel)]="query"
          (keyup.enter)="reload()"
        />
        <select class="form-select" style="width: 200px" [(ngModel)]="categoryId" (change)="reload()">
          <option [ngValue]="null">Toutes les catégories</option>
          @for (c of categories; track c.id) {
            <option [ngValue]="c.id">{{ c.name }}</option>
          }
        </select>
        <button class="btn btn-primary" (click)="reload()">Rechercher</button>
      </div>
    </div>

    @if (loading) {
      <app-loader message="Chargement des produits..." />
    } @else if (products.length === 0) {
      <div class="alert alert-warning text-center">Aucun produit trouvé.</div>
    } @else {
      <div class="row g-4">
        @for (p of products; track p.id) {
          <div class="col-sm-6 col-lg-4 col-xl-3">
            <div class="card h-100 product-card shadow-sm">
              <img [src]="p.imageUrl || 'https://placehold.co/400x300?text=Produit'" [alt]="p.name" />
              <div class="card-body d-flex flex-column">
                <h6 class="card-title mb-1 text-truncate" [title]="p.name">{{ p.name }}</h6>
                <small class="text-muted mb-2">{{ p.categoryName }}</small>
                <div class="mt-auto">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="fw-bold text-primary">{{ p.price | number:'1.2-2' }} MAD</span>
                    <span class="badge bg-{{ p.stock > 0 ? 'success' : 'danger' }}">
                      {{ p.stock > 0 ? p.stock + ' en stock' : 'Rupture' }}
                    </span>
                  </div>
                  <a class="btn btn-outline-primary w-100 btn-sm" [routerLink]="['/product', p.id]">
                    Voir le détail
                  </a>
                </div>
              </div>
            </div>
          </div>
        }
      </div>

      @if (totalPages > 1) {
        <nav class="mt-4 d-flex justify-content-center">
          <ul class="pagination">
            <li class="page-item" [class.disabled]="page === 0">
              <button class="page-link" (click)="goTo(page - 1)">Précédent</button>
            </li>
            @for (i of pageNumbers(); track i) {
              <li class="page-item" [class.active]="i === page">
                <button class="page-link" (click)="goTo(i)">{{ i + 1 }}</button>
              </li>
            }
            <li class="page-item" [class.disabled]="page >= totalPages - 1">
              <button class="page-link" (click)="goTo(page + 1)">Suivant</button>
            </li>
          </ul>
        </nav>
      }
    }
  `
})
export class ProductListComponent implements OnInit {
  private productSvc = inject(ProductService);

  products: Product[] = [];
  categories: Category[] = [];
  page = 0;
  size = 12;
  totalPages = 0;
  query = '';
  categoryId: number | null = null;
  loading = false;

  ngOnInit(): void {
    this.productSvc.categories().subscribe((r) => (this.categories = r.data ?? []));
    this.reload();
  }

  reload(): void {
    this.loading = true;
    this.productSvc
      .list({ q: this.query, categoryId: this.categoryId ?? undefined, page: this.page, size: this.size })
      .subscribe({
        next: (r) => {
          this.products = r.data?.content ?? [];
          this.totalPages = r.data?.totalPages ?? 0;
          this.loading = false;
        },
        error: () => (this.loading = false)
      });
  }

  goTo(p: number): void {
    if (p < 0 || p >= this.totalPages) return;
    this.page = p;
    this.reload();
  }

  pageNumbers(): number[] {
    return Array.from({ length: this.totalPages }, (_, i) => i);
  }
}
