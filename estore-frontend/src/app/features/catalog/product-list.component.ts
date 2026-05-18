import {
  Component,
  OnInit,
  inject,
  signal,
  computed,
  effect
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ProductService, ProductSort } from '../../core/services/product.service';
import { CartService } from '../../core/services/cart.service';
import { ToastService } from '../../core/services/toast.service';
import { AuthService } from '../../core/services/auth.service';
import { Category, Product } from '../../core/models/product.model';
import { LoaderComponent } from '../../shared/components/loader.component';
import { environment } from '../../../environments/environment';
import { Subject, debounceTime, takeUntil } from 'rxjs';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LoaderComponent],
  template: `
    <section class="catalog">
      <!-- ─── Hero ─── -->
      <header class="hero">
        <span class="eyebrow">· CATALOGUE E-STORE</span>
        <h1 class="hero-title">
          Découvrez une sélection <span class="grad-text">premium</span><br />
          pensée pour vous.
        </h1>
        <p class="hero-sub">
          {{ totalCount() }} produits · paiement sécurisé · livraison 48–72h partout au Maroc.
        </p>

        <!-- Catégories en pills -->
        <div class="cat-pills">
          <button
            type="button"
            class="cat-pill"
            [class.active]="filters().categoryId == null"
            (click)="setCategory(null)">
            Toutes
          </button>
          @for (c of categories(); track c.id) {
            <button
              type="button"
              class="cat-pill"
              [class.active]="filters().categoryId === c.id"
              (click)="setCategory(c.id)">
              {{ c.name }}
            </button>
          }
        </div>
      </header>

      <!-- ─── Toolbar ─── -->
      <div class="toolbar">
        <div class="search">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <circle cx="11" cy="11" r="7"/>
            <line x1="21" y1="21" x2="16.5" y2="16.5"/>
          </svg>
          <input
            type="text"
            placeholder="Rechercher un produit…"
            [ngModel]="searchInput()"
            (ngModelChange)="onSearchChange($event)" />
        </div>

        <div class="actions">
          <select class="sort-select input-dark" [ngModel]="filters().sort" (ngModelChange)="setSort($event)">
            <option value="newest">Plus récents</option>
            <option value="oldest">Plus anciens</option>
            <option value="price_asc">Prix croissant</option>
            <option value="price_desc">Prix décroissant</option>
            <option value="name_asc">Nom A → Z</option>
            <option value="name_desc">Nom Z → A</option>
          </select>

          <button class="btn-premium ghost filter-toggle" (click)="filterPanelOpen.set(!filterPanelOpen())">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="4" y1="6" x2="20" y2="6"/>
              <line x1="7" y1="12" x2="17" y2="12"/>
              <line x1="10" y1="18" x2="14" y2="18"/>
            </svg>
            Filtres
            @if (activeFilterCount() > 0) {
              <span class="badge-count">{{ activeFilterCount() }}</span>
            }
          </button>
        </div>
      </div>

      <!-- ─── Panneau filtres rétractable ─── -->
      @if (filterPanelOpen()) {
        <div class="filter-panel">
          <div class="filter-group">
            <label>Prix minimum (MAD)</label>
            <input
              type="number" min="0"
              [ngModel]="filters().minPrice"
              (ngModelChange)="setMinPrice($event)"
              placeholder="0" />
          </div>
          <div class="filter-group">
            <label>Prix maximum (MAD)</label>
            <input
              type="number" min="0"
              [ngModel]="filters().maxPrice"
              (ngModelChange)="setMaxPrice($event)"
              placeholder="—" />
          </div>
          <div class="filter-group switch">
            <label class="check-row">
              <input
                type="checkbox"
                [ngModel]="filters().inStockOnly"
                (ngModelChange)="setInStockOnly($event)" />
              <span>En stock uniquement</span>
            </label>
          </div>
          <button class="btn-premium ghost reset-btn" (click)="resetFilters()">
            Réinitialiser
          </button>
        </div>
      }

      <!-- ─── Grille produits ─── -->
      @if (loading()) {
        <app-loader message="Chargement du catalogue..." />
      } @else if (products().length === 0) {
        <div class="empty">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.4">
            <circle cx="12" cy="12" r="10"/>
            <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
          </svg>
          <h3>Aucun produit ne correspond à votre recherche</h3>
          <p>Essayez d'ajuster vos filtres ou réinitialisez-les pour parcourir tout le catalogue.</p>
          <button class="btn-premium primary" (click)="resetFilters()">Réinitialiser les filtres</button>
        </div>
      } @else {
        <div class="grid">
          @for (p of products(); track p.id) {
            <article class="card-product">
              <a [routerLink]="['/product', p.id]" class="media">
                <img [src]="resolveImage(p.imageUrl)" [alt]="p.name" loading="lazy" (error)="onImgError($event)"/>
                @if (p.stock === 0) {
                  <span class="badge rupture">Rupture</span>
                } @else if (p.stock < 5) {
                  <span class="badge low">Stock faible</span>
                }
                <span class="badge category">{{ p.categoryName }}</span>
              </a>
              <div class="body">
                <a [routerLink]="['/product', p.id]" class="name">{{ p.name }}</a>
                @if (p.description) {
                  <p class="desc">{{ p.description }}</p>
                }
                <div class="row">
                  <span class="price">{{ p.price | number:'1.0-0' }} <small>MAD</small></span>
                  <button
                    class="add-btn"
                    [disabled]="p.stock === 0 || addingId() === p.id"
                    (click)="quickAdd(p)"
                    [title]="p.stock === 0 ? 'En rupture' : 'Ajouter au panier'">
                    @if (addingId() === p.id) {
                      <span class="spin"></span>
                    } @else {
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="12" y1="5" x2="12" y2="19"/>
                        <line x1="5" y1="12" x2="19" y2="12"/>
                      </svg>
                    }
                  </button>
                </div>
              </div>
            </article>
          }
        </div>

        <!-- Pagination -->
        @if (totalPages() > 1) {
          <nav class="pagination">
            <button class="pg-btn" [disabled]="page() === 0" (click)="goTo(page() - 1)">‹</button>
            @for (n of pageNumbers(); track n) {
              <button class="pg-btn" [class.active]="n === page()" (click)="goTo(n)">{{ n + 1 }}</button>
            }
            <button class="pg-btn" [disabled]="page() === totalPages() - 1" (click)="goTo(page() + 1)">›</button>
          </nav>
        }
      }
    </section>
  `,
  styles: [`
    :host { display: block; }

    .catalog {
      max-width: 1340px;
      margin: 0 auto;
      padding: 2.5rem 1.5rem 4rem;
    }

    /* Hero */
    .hero { margin-bottom: 2.5rem; }
    .hero-title {
      font-size: clamp(1.8rem, 4vw, 3rem);
      line-height: 1.05;
      margin: 0.5rem 0 0.8rem;
    }
    .hero-sub {
      color: var(--text-secondary);
      max-width: 560px;
      margin: 0 0 1.5rem;
    }

    /* Pills catégories */
    .cat-pills { display: flex; flex-wrap: wrap; gap: 0.5rem; }
    .cat-pill {
      padding: 0.5rem 1rem;
      font-size: 0.85rem;
      border-radius: 999px;
      border: 1px solid var(--border-soft);
      background: var(--surface);
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: var(--font-body);
    }
    .cat-pill:hover { background: var(--surface-hover); color: var(--text-primary); }
    .cat-pill.active {
      background: var(--accent-grad);
      border-color: transparent;
      color: var(--text-inverse);
      font-weight: 600;
    }

    /* Toolbar */
    .toolbar {
      display: flex; gap: 1rem; align-items: center; justify-content: space-between;
      padding: 0.8rem 0; margin-bottom: 1rem;
      border-top: 1px solid var(--border-soft);
      border-bottom: 1px solid var(--border-soft);
      flex-wrap: wrap;
    }
    .search {
      display: flex; align-items: center; gap: 0.5rem; flex: 1; min-width: 260px;
      padding: 0.55rem 0.95rem;
      background: var(--bg-elev-1);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-sm);
      color: var(--text-tertiary);
    }
    .search input {
      flex: 1; background: transparent; border: none; outline: none;
      color: var(--text-primary); font-family: var(--font-body);
    }
    .actions { display: flex; gap: 0.6rem; align-items: center; }
    .sort-select { min-width: 180px; }
    .filter-toggle { position: relative; }
    .badge-count {
      display: inline-flex; align-items: center; justify-content: center;
      min-width: 18px; height: 18px; padding: 0 5px;
      background: var(--accent-grad); color: var(--text-inverse);
      border-radius: 999px; font-size: 0.7rem; font-weight: 700; margin-left: 0.3rem;
    }

    /* Filter panel */
    .filter-panel {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem; padding: 1.2rem;
      background: var(--bg-elev-1);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-md);
      margin-bottom: 1.4rem;
      align-items: end;
    }
    .filter-group label {
      display: block; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em;
      color: var(--text-tertiary); margin-bottom: 0.4rem;
    }
    .filter-group input[type=number] {
      width: 100%; padding: 0.5rem 0.75rem;
      background: var(--bg-base); color: var(--text-primary);
      border: 1px solid var(--border-soft); border-radius: var(--radius-sm);
      font-family: var(--font-body);
    }
    .check-row { display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary); cursor: pointer; }
    .check-row input { accent-color: var(--accent-blue); width: 16px; height: 16px; }
    .reset-btn { width: 100%; }

    /* Empty */
    .empty {
      text-align: center; padding: 4rem 1rem;
      background: var(--bg-elev-1);
      border: 1px dashed var(--border-soft);
      border-radius: var(--radius-md);
      color: var(--text-secondary);
    }
    .empty h3 { font-size: 1.2rem; margin: 1rem 0 0.4rem; }
    .empty p { max-width: 380px; margin: 0 auto 1.2rem; font-size: 0.92rem; }

    /* Grid */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 1.4rem;
    }

    /* Card */
    .card-product {
      display: flex; flex-direction: column;
      background: var(--bg-elev-1);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-md);
      overflow: hidden;
      transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.4s ease;
    }
    .card-product:hover {
      transform: translateY(-4px);
      border-color: var(--border-strong);
      box-shadow: var(--shadow-soft);
    }

    .media {
      position: relative; aspect-ratio: 1 / 1;
      background: var(--bg-elev-2);
      overflow: hidden;
      display: block;
    }
    .media img {
      width: 100%; height: 100%;
      object-fit: cover;
      transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    .card-product:hover .media img { transform: scale(1.05); }

    .badge {
      position: absolute; top: 0.7rem; left: 0.7rem;
      padding: 0.25rem 0.65rem;
      font-size: 0.7rem; font-weight: 600; letter-spacing: 0.05em;
      border-radius: 999px;
      backdrop-filter: blur(8px);
    }
    .badge.rupture {
      background: rgba(239, 68, 68, 0.18);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.35);
    }
    .badge.low {
      background: rgba(245, 158, 11, 0.18);
      color: #fcd34d;
      border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .badge.category {
      top: auto; bottom: 0.7rem; left: 0.7rem;
      background: rgba(14, 16, 18, 0.65);
      color: var(--text-primary);
      border: 1px solid var(--border-soft);
    }

    .body { padding: 1rem 1.1rem 1.1rem; display: flex; flex-direction: column; gap: 0.45rem; flex: 1; }
    .name {
      font-family: var(--font-display);
      font-size: 1.05rem; font-weight: 600;
      color: var(--text-primary);
      text-decoration: none;
      line-height: 1.25;
      transition: color 0.2s ease;
    }
    .name:hover { color: var(--accent-cyan); }
    .desc {
      font-size: 0.85rem; color: var(--text-secondary);
      margin: 0; line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .row { margin-top: auto; padding-top: 0.5rem; display: flex; justify-content: space-between; align-items: center; }
    .price {
      font-family: var(--font-display);
      font-size: 1.2rem; font-weight: 700;
      background: var(--accent-grad);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .price small { font-size: 0.7rem; opacity: 0.7; }

    .add-btn {
      width: 38px; height: 38px;
      display: inline-flex; align-items: center; justify-content: center;
      background: var(--surface);
      color: var(--text-primary);
      border: 1px solid var(--border-soft);
      border-radius: 50%;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .add-btn:hover:not(:disabled) {
      background: var(--accent-grad);
      color: var(--text-inverse);
      border-color: transparent;
      transform: scale(1.05);
    }
    .add-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .spin {
      width: 14px; height: 14px;
      border: 2px solid currentColor;
      border-right-color: transparent;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* Pagination */
    .pagination { display: flex; justify-content: center; gap: 0.4rem; margin-top: 2.4rem; }
    .pg-btn {
      min-width: 36px; height: 36px;
      padding: 0 0.7rem;
      background: var(--bg-elev-1);
      color: var(--text-secondary);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-sm);
      cursor: pointer;
      font-family: var(--font-body);
      transition: all 0.2s ease;
    }
    .pg-btn:hover:not(:disabled) { background: var(--surface-hover); color: var(--text-primary); }
    .pg-btn:disabled { opacity: 0.35; cursor: not-allowed; }
    .pg-btn.active {
      background: var(--accent-grad);
      color: var(--text-inverse);
      border-color: transparent;
      font-weight: 600;
    }
  `]
})
export class ProductListComponent implements OnInit {
  private svc = inject(ProductService);
  private cartSvc = inject(CartService);
  private toast = inject(ToastService);
  private auth = inject(AuthService);

  loading = signal(true);
  products = signal<Product[]>([]);
  categories = signal<Category[]>([]);
  totalCount = signal(0);
  totalPages = signal(0);
  page = signal(0);
  size = 12;

  addingId = signal<number | null>(null);
  filterPanelOpen = signal(false);

  searchInput = signal('');
  filters = signal<{
    q: string;
    categoryId: number | null;
    sort: ProductSort;
    minPrice: number | null;
    maxPrice: number | null;
    inStockOnly: boolean;
  }>({
    q: '',
    categoryId: null,
    sort: 'newest',
    minPrice: null,
    maxPrice: null,
    inStockOnly: false
  });

  activeFilterCount = computed(() => {
    const f = this.filters();
    let n = 0;
    if (f.minPrice != null && !Number.isNaN(f.minPrice)) n++;
    if (f.maxPrice != null && !Number.isNaN(f.maxPrice)) n++;
    if (f.inStockOnly) n++;
    return n;
  });

  private searchSubject = new Subject<string>();
  private destroy$ = new Subject<void>();

  constructor() {
    // Debounce de la recherche
    this.searchSubject.pipe(debounceTime(350), takeUntil(this.destroy$)).subscribe((q) => {
      this.filters.update((f) => ({ ...f, q }));
      this.page.set(0);
      this.fetch();
    });

    // Refetch automatique à chaque changement de filtre
    effect(() => {
      this.filters();
      this.page();
      // l'effet déclenche fetch via les setters; on ne le rappelle pas ici pour éviter double appel
    });
  }

  ngOnInit(): void {
    this.svc.categories().subscribe({
      next: (r) => this.categories.set(r.data ?? [])
    });
    this.fetch();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  fetch(): void {
    this.loading.set(true);
    const f = this.filters();
    this.svc
      .list({
        q: f.q || undefined,
        categoryId: f.categoryId ?? undefined,
        minPrice: f.minPrice ?? undefined,
        maxPrice: f.maxPrice ?? undefined,
        inStockOnly: f.inStockOnly,
        sort: f.sort,
        page: this.page(),
        size: this.size
      })
      .subscribe({
        next: (r) => {
          this.products.set(r.data?.content ?? []);
          this.totalPages.set(r.data?.totalPages ?? 0);
          this.totalCount.set(r.data?.totalElements ?? 0);
          this.loading.set(false);
        },
        error: () => {
          this.loading.set(false);
          this.toast.error('Impossible de charger le catalogue');
        }
      });
  }

  onSearchChange(v: string): void {
    this.searchInput.set(v);
    this.searchSubject.next(v);
  }

  setCategory(id: number | null): void {
    this.filters.update((f) => ({ ...f, categoryId: id }));
    this.page.set(0);
    this.fetch();
  }

  setSort(s: ProductSort): void {
    this.filters.update((f) => ({ ...f, sort: s }));
    this.fetch();
  }

  setMinPrice(v: number | null): void {
    this.filters.update((f) => ({ ...f, minPrice: v == null ? null : Number(v) }));
    this.fetch();
  }

  setMaxPrice(v: number | null): void {
    this.filters.update((f) => ({ ...f, maxPrice: v == null ? null : Number(v) }));
    this.fetch();
  }

  setInStockOnly(b: boolean): void {
    this.filters.update((f) => ({ ...f, inStockOnly: b }));
    this.fetch();
  }

  resetFilters(): void {
    this.filters.set({
      q: '',
      categoryId: null,
      sort: 'newest',
      minPrice: null,
      maxPrice: null,
      inStockOnly: false
    });
    this.searchInput.set('');
    this.page.set(0);
    this.fetch();
  }

  goTo(p: number): void {
    if (p < 0 || p >= this.totalPages()) return;
    this.page.set(p);
    this.fetch();
  }

  pageNumbers(): number[] {
    return Array.from({ length: this.totalPages() }, (_, i) => i);
  }

  quickAdd(p: Product): void {
    if (!this.auth.isAuthenticated) {
      this.toast.info('Connectez-vous pour ajouter au panier');
      return;
    }
    this.addingId.set(p.id);
    this.cartSvc.add(p.id, 1).subscribe({
      next: () => {
        this.toast.success(`${p.name} ajouté au panier`);
        this.addingId.set(null);
      },
      error: () => {
        this.toast.error('Erreur lors de l\'ajout');
        this.addingId.set(null);
      }
    });
  }

  resolveImage(url?: string): string {
    if (!url) return this.placeholder();
    if (url.startsWith('http://') || url.startsWith('https://')) return url;
    if (url.startsWith('/uploads/')) return `${environment.apiUrl.replace('/api', '')}${url}`;
    return url;
  }

  onImgError(e: Event): void {
    const img = e.target as HTMLImageElement;
    img.src = this.placeholder();
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
