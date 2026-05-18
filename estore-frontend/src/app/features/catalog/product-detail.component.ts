import { Component, OnInit, inject, signal, computed } from '@angular/core';
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
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LoaderComponent, ReviewFormComponent],
  template: `
    @if (loading()) {
      <app-loader message="Chargement du produit..." />
    } @else if (product()) {
      <div class="detail">
        <a routerLink="/" class="back-link">← Retour au catalogue</a>

        <section class="hero-detail">
          <div class="media-frame">
            <img [src]="resolveImage(product()!.imageUrl)" [alt]="product()!.name" (error)="onImgError($event)" />
            <span class="cat-tag">{{ product()!.categoryName }}</span>
          </div>

          <div class="info">
            <h1 class="title">{{ product()!.name }}</h1>

            @if (avgRating() > 0) {
              <div class="rating">
                @for (s of starArray(); track $index) {
                  <span class="star" [class.filled]="s">★</span>
                }
                <span class="rating-text">{{ avgRating() | number:'1.1-1' }} · {{ reviews().length }} avis</span>
              </div>
            }

            <p class="price">
              {{ product()!.price | number:'1.0-0' }}
              <small>MAD</small>
            </p>

            <p class="desc">{{ product()!.description || 'Aucune description fournie.' }}</p>

            <!-- Stock pill -->
            <div class="stock-pill" [ngClass]="stockClass()">
              <span class="dot"></span>
              {{ stockLabel() }}
            </div>

            <!-- Quantity + CTA -->
            @if (product()!.stock > 0) {
              <div class="qty-row">
                <div class="qty">
                  <button type="button" (click)="dec()" [disabled]="qty() === 1">−</button>
                  <input type="number" min="1" [max]="product()!.stock" [ngModel]="qty()" (ngModelChange)="setQty($event)" />
                  <button type="button" (click)="inc()" [disabled]="qty() >= product()!.stock">+</button>
                </div>
                <button class="btn-premium primary cta" [disabled]="adding()" (click)="addToCart()">
                  @if (adding()) {
                    <span class="spin"></span>
                  } @else {
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="9" cy="21" r="1"/>
                      <circle cx="20" cy="21" r="1"/>
                      <path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>
                    </svg>
                    <span>Ajouter — {{ (product()!.price * qty()) | number:'1.0-0' }} MAD</span>
                  }
                </button>
              </div>
            }

            <!-- Trust badges -->
            <ul class="trust">
              <li>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                Paiement sécurisé
              </li>
              <li>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
                Livraison 48–72h
              </li>
              <li>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
                Retour 14 jours
              </li>
            </ul>
          </div>
        </section>

        <!-- Reviews -->
        <section class="reviews">
          <header>
            <h2>Avis clients</h2>
            <span class="muted">{{ reviews().length }} avis</span>
          </header>

          @if (auth.isAuthenticated) {
            <app-review-form [productId]="product()!.id" (saved)="loadReviews()" />
          } @else {
            <p class="muted">
              <a routerLink="/login">Connectez-vous</a> pour laisser un avis.
            </p>
          }

          @if (reviews().length === 0) {
            <p class="muted empty-rev">Soyez le premier à donner votre avis sur ce produit.</p>
          } @else {
            <ul class="rev-list">
              @for (r of reviews(); track r.id) {
                <li class="rev">
                  <div class="avatar">{{ initials(r.authorName) }}</div>
                  <div class="rev-body">
                    <header>
                      <strong>{{ r.authorName }}</strong>
                      <span class="muted small">{{ r.createdAt | date:'dd MMM yyyy' }}</span>
                    </header>
                    <div class="rev-stars">
                      @for (i of [0,1,2,3,4]; track i) {
                        <span class="star" [class.filled]="i < r.rating">★</span>
                      }
                    </div>
                    <p>{{ r.comment }}</p>
                  </div>
                </li>
              }
            </ul>
          }
        </section>
      </div>
    } @else {
      <div class="not-found">
        <h2>Produit introuvable</h2>
        <a routerLink="/" class="btn-premium primary">Retour au catalogue</a>
      </div>
    }
  `,
  styles: [`
    :host { display: block; }
    .detail { max-width: 1240px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
    .back-link { color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; display: inline-block; margin-bottom: 1.5rem; }
    .back-link:hover { color: var(--accent-cyan); }

    .hero-detail {
      display: grid; grid-template-columns: minmax(280px, 1fr) 1fr;
      gap: 2.5rem; align-items: start;
    }
    @media (max-width: 860px) { .hero-detail { grid-template-columns: 1fr; } }

    .media-frame {
      position: relative; aspect-ratio: 1 / 1;
      background: var(--bg-elev-1);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-lg);
      overflow: hidden;
    }
    .media-frame img { width: 100%; height: 100%; object-fit: cover; }
    .cat-tag {
      position: absolute; top: 1rem; left: 1rem;
      padding: 0.3rem 0.85rem;
      background: rgba(14, 16, 18, 0.7);
      border: 1px solid var(--border-soft);
      backdrop-filter: blur(8px);
      border-radius: 999px;
      font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase;
      color: var(--text-primary);
    }

    .info { display: flex; flex-direction: column; gap: 1.1rem; }
    .title { font-size: clamp(1.6rem, 3vw, 2.4rem); margin: 0; line-height: 1.1; }

    .rating { display: flex; align-items: center; gap: 0.4rem; }
    .star { color: var(--text-tertiary); }
    .star.filled { color: #fbbf24; }
    .rating-text { color: var(--text-secondary); font-size: 0.85rem; margin-left: 0.3rem; }

    .price {
      font-family: var(--font-display);
      font-size: 2.2rem; font-weight: 700;
      margin: 0;
      background: var(--accent-grad);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .price small { font-size: 1rem; opacity: 0.7; }

    .desc { color: var(--text-secondary); line-height: 1.6; margin: 0; }

    .stock-pill {
      display: inline-flex; align-items: center; gap: 0.5rem;
      padding: 0.4rem 0.9rem;
      border-radius: 999px;
      font-size: 0.85rem; font-weight: 500;
      width: fit-content;
    }
    .stock-pill .dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; animation: pulse-dot 1.6s ease-in-out infinite; }
    .stock-pill.ok    { background: rgba(16, 185, 129, 0.14); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.32); }
    .stock-pill.low   { background: rgba(245, 158, 11, 0.14); color: #fcd34d; border: 1px solid rgba(245, 158, 11, 0.32); }
    .stock-pill.out   { background: rgba(239, 68, 68, 0.14);  color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.32); }
    @keyframes pulse-dot { 50% { transform: scale(1.4); opacity: 0.6; } }

    .qty-row { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; margin-top: 0.5rem; }
    .qty {
      display: inline-flex; align-items: center;
      background: var(--bg-elev-1);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-sm);
      overflow: hidden;
    }
    .qty button {
      width: 38px; height: 40px;
      background: transparent; color: var(--text-primary);
      border: none; cursor: pointer; font-size: 1.1rem;
      transition: background 0.2s ease;
    }
    .qty button:hover:not(:disabled) { background: var(--surface-hover); }
    .qty button:disabled { opacity: 0.35; cursor: not-allowed; }
    .qty input {
      width: 60px; text-align: center;
      background: transparent; color: var(--text-primary);
      border: none; outline: none;
      font-family: var(--font-display);
    }
    .cta { padding: 0.8rem 1.4rem; }
    .spin {
      width: 14px; height: 14px;
      border: 2px solid currentColor; border-right-color: transparent;
      border-radius: 50%; animation: spin 0.7s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    .trust {
      display: flex; flex-wrap: wrap; gap: 1.2rem;
      list-style: none; padding: 1rem 0 0; margin: 1rem 0 0;
      border-top: 1px solid var(--border-soft);
      color: var(--text-secondary); font-size: 0.85rem;
    }
    .trust li { display: inline-flex; align-items: center; gap: 0.5rem; }

    /* Reviews */
    .reviews { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border-soft); }
    .reviews > header { display: flex; align-items: baseline; gap: 1rem; margin-bottom: 1.4rem; }
    .reviews h2 { font-size: 1.4rem; margin: 0; }
    .muted { color: var(--text-tertiary); font-size: 0.85rem; }
    .muted.small { font-size: 0.78rem; }
    .empty-rev { padding: 1.5rem 0; }

    .rev-list { list-style: none; padding: 0; margin: 1.4rem 0 0; display: flex; flex-direction: column; gap: 1rem; }
    .rev {
      display: grid; grid-template-columns: 40px 1fr; gap: 0.9rem;
      padding: 1rem 1.1rem;
      background: var(--bg-elev-1);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-md);
    }
    .avatar {
      width: 40px; height: 40px;
      display: inline-flex; align-items: center; justify-content: center;
      background: var(--accent-grad);
      color: var(--text-inverse);
      font-family: var(--font-display);
      font-weight: 700;
      border-radius: 50%;
    }
    .rev-body header { display: flex; align-items: baseline; gap: 0.6rem; }
    .rev-stars { margin: 0.2rem 0 0.4rem; }
    .rev p { margin: 0; color: var(--text-secondary); line-height: 1.5; }

    .not-found { text-align: center; padding: 5rem 1rem; }
    .not-found h2 { margin-bottom: 1.5rem; }
  `]
})
export class ProductDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private productSvc = inject(ProductService);
  private cartSvc = inject(CartService);
  private reviewSvc = inject(ReviewService);
  private toast = inject(ToastService);
  auth = inject(AuthService);

  loading = signal(true);
  product = signal<Product | null>(null);
  reviews = signal<Review[]>([]);
  qty = signal(1);
  adding = signal(false);

  avgRating = computed(() => {
    const list = this.reviews();
    if (list.length === 0) return 0;
    return list.reduce((sum, r) => sum + r.rating, 0) / list.length;
  });

  starArray = computed(() => {
    const avg = Math.round(this.avgRating());
    return [0, 1, 2, 3, 4].map((i) => i < avg);
  });

  stockClass = computed(() => {
    const s = this.product()?.stock ?? 0;
    if (s === 0) return 'out';
    if (s < 5) return 'low';
    return 'ok';
  });

  stockLabel = computed(() => {
    const s = this.product()?.stock ?? 0;
    if (s === 0) return 'Rupture de stock';
    if (s < 5) return `Plus que ${s} en stock`;
    return 'En stock';
  });

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.fetch(id);
    this.reviewSvc.byProduct(id).subscribe({
      next: (r) => this.reviews.set(r.data ?? [])
    });
  }

  fetch(id: number): void {
    this.productSvc.getById(id).subscribe({
      next: (r) => {
        this.product.set(r.data ?? null);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.toast.error('Produit introuvable');
      }
    });
  }

  loadReviews(): void {
    const p = this.product();
    if (!p) return;
    this.reviewSvc.byProduct(p.id).subscribe({
      next: (r) => this.reviews.set(r.data ?? [])
    });
  }

  inc(): void {
    const max = this.product()?.stock ?? 1;
    this.qty.update((v) => Math.min(v + 1, max));
  }

  dec(): void {
    this.qty.update((v) => Math.max(v - 1, 1));
  }

  setQty(v: number): void {
    const max = this.product()?.stock ?? 1;
    this.qty.set(Math.max(1, Math.min(Number(v) || 1, max)));
  }

  addToCart(): void {
    const p = this.product();
    if (!p) return;
    if (!this.auth.isAuthenticated) {
      this.toast.info('Connectez-vous pour ajouter au panier');
      this.router.navigate(['/login']);
      return;
    }
    this.adding.set(true);
    this.cartSvc.add(p.id, this.qty()).subscribe({
      next: () => {
        this.toast.success(`${p.name} ajouté au panier`);
        this.adding.set(false);
      },
      error: () => {
        this.toast.error('Erreur lors de l\'ajout');
        this.adding.set(false);
      }
    });
  }

  initials(name: string): string {
    return name
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 2)
      .map((s) => s[0]?.toUpperCase() ?? '')
      .join('');
  }

  resolveImage(url?: string): string {
    if (!url) return this.placeholder();
    if (url.startsWith('http://') || url.startsWith('https://')) return url;
    if (url.startsWith('/uploads/')) return `${environment.apiUrl.replace('/api', '')}${url}`;
    return url;
  }

  onImgError(e: Event): void {
    (e.target as HTMLImageElement).src = this.placeholder();
  }

  private placeholder(): string {
    return 'data:image/svg+xml;utf8,' + encodeURIComponent(
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
        <rect width="400" height="400" fill="#1c2024"/>
        <text x="50%" y="50%" font-family="sans-serif" font-size="20" fill="#6c7178" text-anchor="middle" dy=".3em">Image indisponible</text>
      </svg>`
    );
  }
}
