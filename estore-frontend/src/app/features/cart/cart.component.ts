import { Component, OnInit, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CartService } from '../../core/services/cart.service';
import { ToastService } from '../../core/services/toast.service';
import { LoaderComponent } from '../../shared/components/loader.component';
import { environment } from '../../../environments/environment';

const FREE_SHIPPING_THRESHOLD = 500;
const FLAT_SHIPPING = 40;
const TAX_RATE = 0.2;

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LoaderComponent],
  template: `
    <section class="cart">
      <header class="cart-head">
        <span class="eyebrow">· VOTRE PANIER</span>
        <h1>Mon panier</h1>
      </header>

      @if (loading) {
        <app-loader message="Chargement du panier..." />
      } @else if (!cartSvc.cart() || cartSvc.cart()!.items.length === 0) {
        <div class="empty">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.4">
            <circle cx="9" cy="21" r="1"/>
            <circle cx="20" cy="21" r="1"/>
            <path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>
          </svg>
          <h3>Votre panier est vide</h3>
          <p>Parcourez notre catalogue pour découvrir nos produits premium.</p>
          <a class="btn-premium primary" routerLink="/">Voir le catalogue</a>
        </div>
      } @else {
        <div class="layout">
          <!-- ── Items ── -->
          <div class="items">
            @for (item of cartSvc.cart()!.items; track item.id) {
              <article class="item">
                <div class="thumb">
                  <img [src]="resolveImage(item.imageUrl)" [alt]="item.productName" (error)="onImgError($event)" />
                </div>
                <div class="meta">
                  <a class="name" [routerLink]="['/product', item.productId]">{{ item.productName }}</a>
                  <span class="unit">{{ item.unitPrice | number:'1.0-0' }} MAD / pièce</span>

                  <div class="qty-row">
                    <div class="qty">
                      <button type="button" (click)="dec(item.id, item.quantity)" [disabled]="item.quantity === 1">−</button>
                      <input
                        type="number" min="1"
                        [ngModel]="item.quantity"
                        (ngModelChange)="setQty(item.id, $event)" />
                      <button type="button" (click)="inc(item.id, item.quantity)">+</button>
                    </div>
                    <button class="remove" (click)="remove(item.id)" title="Retirer">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                      </svg>
                    </button>
                  </div>
                </div>
                <span class="line-total">{{ item.subtotal | number:'1.0-0' }} <small>MAD</small></span>
              </article>
            }
          </div>

          <!-- ── Summary ── -->
          <aside class="summary">
            <h3>Récapitulatif</h3>

            @if (subtotal() < FREE_SHIPPING) {
              <div class="ship-progress">
                <p>
                  Plus que <strong>{{ (FREE_SHIPPING - subtotal()) | number:'1.0-0' }} MAD</strong>
                  pour la livraison gratuite
                </p>
                <div class="bar"><span [style.width.%]="shipProgress()"></span></div>
              </div>
            } @else {
              <div class="ship-free">
                ✓ Vous bénéficiez de la livraison gratuite
              </div>
            }

            <div class="row">
              <span>Sous-total</span>
              <strong>{{ subtotal() | number:'1.0-0' }} MAD</strong>
            </div>
            <div class="row">
              <span>Livraison</span>
              <strong>
                @if (shipping() === 0) { <span class="ok">Gratuite</span> }
                @else { {{ shipping() }} MAD }
              </strong>
            </div>
            <div class="row">
              <span>TVA (20%)</span>
              <strong>{{ tax() | number:'1.0-0' }} MAD</strong>
            </div>
            <div class="row total">
              <span>Total</span>
              <strong>{{ total() | number:'1.0-0' }} MAD</strong>
            </div>

            <button class="btn-premium primary go-checkout" (click)="proceedToCheckout()">
              Passer au paiement →
            </button>

            <a routerLink="/" class="continue">← Continuer mes achats</a>
          </aside>
        </div>
      }
    </section>
  `,
  styles: [`
    :host { display: block; }
    .cart { max-width: 1240px; margin: 0 auto; padding: 2.5rem 1.5rem 4rem; }
    .cart-head { margin-bottom: 2rem; }
    .cart-head h1 { font-size: clamp(1.8rem, 3vw, 2.4rem); margin: 0.4rem 0 0; }

    .empty {
      text-align: center; padding: 4rem 1rem;
      background: var(--bg-elev-1);
      border: 1px dashed var(--border-soft);
      border-radius: var(--radius-md);
      color: var(--text-secondary);
    }
    .empty h3 { font-size: 1.3rem; margin: 1rem 0 0.4rem; color: var(--text-primary); }
    .empty p { margin: 0 auto 1.4rem; max-width: 380px; }

    .layout {
      display: grid; grid-template-columns: minmax(0, 1fr) 360px;
      gap: 1.8rem;
    }
    @media (max-width: 880px) { .layout { grid-template-columns: 1fr; } }

    /* Items */
    .items { display: flex; flex-direction: column; gap: 1rem; }
    .item {
      display: grid;
      grid-template-columns: 100px 1fr auto;
      gap: 1.1rem;
      padding: 1rem;
      background: var(--bg-elev-1);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-md);
      align-items: center;
    }
    .thumb {
      width: 100px; height: 100px;
      background: var(--bg-elev-2);
      border-radius: var(--radius-sm);
      overflow: hidden;
    }
    .thumb img { width: 100%; height: 100%; object-fit: cover; }

    .meta { display: flex; flex-direction: column; gap: 0.4rem; min-width: 0; }
    .name {
      font-family: var(--font-display);
      font-weight: 600; color: var(--text-primary);
      text-decoration: none;
    }
    .name:hover { color: var(--accent-cyan); }
    .unit { color: var(--text-tertiary); font-size: 0.82rem; }

    .qty-row { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
    .qty {
      display: inline-flex; align-items: center;
      background: var(--bg-base);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-sm); overflow: hidden;
    }
    .qty button {
      width: 30px; height: 32px;
      background: transparent; color: var(--text-primary);
      border: none; cursor: pointer;
    }
    .qty button:hover:not(:disabled) { background: var(--surface-hover); }
    .qty button:disabled { opacity: 0.35; }
    .qty input {
      width: 42px; text-align: center;
      background: transparent; color: var(--text-primary);
      border: none; outline: none; font-family: var(--font-display);
    }
    .remove {
      width: 32px; height: 32px;
      background: transparent;
      color: var(--text-tertiary);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex; align-items: center; justify-content: center;
    }
    .remove:hover { color: #fca5a5; border-color: rgba(239, 68, 68, 0.4); }

    .line-total {
      font-family: var(--font-display);
      font-weight: 700; font-size: 1.05rem;
      color: var(--text-primary);
      white-space: nowrap;
    }
    .line-total small { color: var(--text-tertiary); font-size: 0.7rem; margin-left: 0.2rem; }

    /* Summary */
    .summary {
      position: sticky; top: 1rem;
      padding: 1.4rem;
      background: var(--bg-elev-1);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-lg);
      height: fit-content;
    }
    .summary h3 { margin: 0 0 1rem; font-size: 1.05rem; letter-spacing: 0.05em; text-transform: uppercase; color: var(--text-tertiary); }

    .ship-progress { padding: 0.8rem 0 1rem; border-bottom: 1px solid var(--border-soft); margin-bottom: 0.8rem; }
    .ship-progress p { color: var(--text-secondary); font-size: 0.85rem; margin: 0 0 0.5rem; }
    .ship-progress .bar {
      height: 6px; background: var(--bg-elev-2); border-radius: 999px; overflow: hidden;
    }
    .ship-progress .bar span {
      display: block; height: 100%;
      background: var(--accent-grad);
      transition: width 0.4s ease;
    }
    .ship-free {
      padding: 0.6rem 0.85rem;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #6ee7b7;
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      margin-bottom: 0.8rem;
    }

    .row { display: flex; justify-content: space-between; padding: 0.4rem 0; color: var(--text-secondary); }
    .row strong { color: var(--text-primary); font-weight: 500; }
    .row .ok { color: #6ee7b7; }
    .row.total {
      margin-top: 0.6rem;
      padding-top: 0.8rem;
      border-top: 1px solid var(--border-soft);
      font-size: 1.05rem;
    }
    .row.total strong {
      font-family: var(--font-display);
      font-size: 1.4rem;
      background: var(--accent-grad);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .go-checkout { width: 100%; margin-top: 1.1rem; padding: 0.85rem; }
    .continue {
      display: block; text-align: center;
      margin-top: 0.8rem; color: var(--text-tertiary); font-size: 0.85rem;
      text-decoration: none;
    }
    .continue:hover { color: var(--accent-cyan); }
  `]
})
export class CartComponent implements OnInit {
  cartSvc = inject(CartService);
  private router = inject(Router);
  private toast = inject(ToastService);

  loading = true;
  readonly FREE_SHIPPING = FREE_SHIPPING_THRESHOLD;

  subtotal = computed(() => this.cartSvc.cart()?.total ?? 0);
  shipping = computed(() => (this.subtotal() >= FREE_SHIPPING_THRESHOLD ? 0 : FLAT_SHIPPING));
  tax = computed(() => Math.round(this.subtotal() * TAX_RATE));
  total = computed(() => Math.round(this.subtotal() + this.shipping() + this.tax()));
  shipProgress = computed(() =>
    Math.min(100, Math.round((this.subtotal() / FREE_SHIPPING_THRESHOLD) * 100))
  );

  ngOnInit(): void {
    this.cartSvc.get().subscribe({
      next: () => (this.loading = false),
      error: () => {
        this.loading = false;
        this.toast.error('Erreur lors du chargement du panier');
      }
    });
  }

  inc(id: number, q: number): void {
    this.setQty(id, q + 1);
  }

  dec(id: number, q: number): void {
    if (q <= 1) return;
    this.setQty(id, q - 1);
  }

  setQty(id: number, q: number): void {
    const qty = Math.max(1, Number(q) || 1);
    this.cartSvc.updateItem(id, qty).subscribe({
      error: () => this.toast.error('Erreur de mise à jour')
    });
  }

  remove(id: number): void {
    this.cartSvc.remove(id).subscribe({
      next: () => this.toast.success('Article retiré'),
      error: () => this.toast.error('Erreur lors du retrait')
    });
  }

  proceedToCheckout(): void {
    this.router.navigate(['/checkout']);
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
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
        <rect width="200" height="200" fill="#1c2024"/>
        <text x="50%" y="50%" font-family="sans-serif" font-size="14" fill="#6c7178" text-anchor="middle" dy=".3em">—</text>
      </svg>`
    );
  }
}
