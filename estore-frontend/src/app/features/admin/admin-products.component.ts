import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ProductService, AdminProductPayload } from '../../core/services/product.service';
import { Category, Product } from '../../core/models/product.model';
import { ToastService } from '../../core/services/toast.service';
import { LoaderComponent } from '../../shared/components/loader.component';
import { environment } from '../../../environments/environment';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-admin-products',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, LoaderComponent],
  template: `
    <div class="admin">
      <header class="admin-head">
        <div>
          <span class="eyebrow">· ESPACE ADMINISTRATEUR</span>
          <h1>Gestion des produits</h1>
          <p class="lead">Créez, modifiez, supprimez et gérez le stock de votre catalogue. Génération d'images photo studio via Gemini Nano Banana.</p>
        </div>
        <button class="btn-premium primary" (click)="openCreate()">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M7 1V13M1 7H13" stroke-linecap="round"/>
          </svg>
          Nouveau produit
        </button>
      </header>

      <div class="stats-row">
        <div class="stat-card">
          <span class="stat-label">Produits</span>
          <span class="stat-value">{{ products.length }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">En rupture</span>
          <span class="stat-value text-warn">{{ countOutOfStock() }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Stock faible (&lt; 5)</span>
          <span class="stat-value text-low">{{ countLowStock() }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Valeur catalogue</span>
          <span class="stat-value grad">{{ totalValue() | number:'1.0-0' }} MAD</span>
        </div>
      </div>

      @if (loading()) {
        <div class="loading-wrap"><app-loader message="Chargement des produits..." /></div>
      } @else {
        <div class="table-wrap">
          <table class="admin-table">
            <thead>
              <tr>
                <th class="img-col">Visuel</th>
                <th>Nom</th>
                <th>Catégorie</th>
                <th class="num">Prix</th>
                <th class="stock-col">Stock</th>
                <th class="actions-col">Actions</th>
              </tr>
            </thead>
            <tbody>
              @for (p of products; track p.id) {
                <tr>
                  <td>
                    <div class="thumb">
                      <img [src]="resolveImage(p.imageUrl)" [alt]="p.name" (error)="onImgError($event)" />
                    </div>
                  </td>
                  <td>
                    <div class="name-cell">
                      <strong>{{ p.name }}</strong>
                      @if (p.description) {
                        <span class="muted">{{ p.description }}</span>
                      }
                    </div>
                  </td>
                  <td>
                    <span class="cat-tag">{{ p.categoryName }}</span>
                  </td>
                  <td class="num">
                    <span class="price-cell">{{ p.price | number:'1.0-0' }} <small>MAD</small></span>
                  </td>
                  <td>
                    <div class="stock-cell">
                      <button class="stock-btn" (click)="decStock(p)" [disabled]="p.stock <= 0 || savingStockId() === p.id" aria-label="Diminuer">−</button>
                      <input
                        type="number"
                        min="0"
                        [value]="p.stock"
                        (change)="setStock(p, $any($event.target).value)"
                        [class.warn]="p.stock < 5"
                        [class.danger]="p.stock === 0"
                      />
                      <button class="stock-btn" (click)="incStock(p)" [disabled]="savingStockId() === p.id" aria-label="Augmenter">+</button>
                    </div>
                  </td>
                  <td>
                    <div class="actions">
                      <button class="icon-btn" (click)="generateImage(p)" [disabled]="generatingId() === p.id" title="Générer image via Gemini">
                        @if (generatingId() === p.id) {
                          <span class="spin"></span>
                        } @else {
                          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5">
                            <rect x="1" y="2" width="12" height="10" rx="1.5"/>
                            <circle cx="5" cy="5" r="1"/>
                            <path d="M13 9L9 6L1 12" stroke-linejoin="round"/>
                          </svg>
                        }
                      </button>
                      <button class="icon-btn" (click)="openEdit(p)" title="Éditer">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M10 2L12 4L5 11L2 12L3 9L10 2Z" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </button>
                      <button class="icon-btn danger" (click)="confirmDelete(p)" title="Supprimer">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M2 4H12M5 4V2H9V4M3 4L4 12H10L11 4" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              } @empty {
                <tr>
                  <td colspan="6" class="empty">Aucun produit. Créez le premier !</td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      }

      <!-- ─── Drawer create/edit ──────────────── -->
      @if (drawerOpen()) {
        <div class="drawer-backdrop" (click)="closeDrawer()"></div>
        <aside class="drawer" [class.editing]="editingId() != null">
          <header class="drawer-head">
            <div>
              <span class="eyebrow">· {{ editingId() ? 'ÉDITION' : 'NOUVEAU PRODUIT' }}</span>
              <h2>{{ editingId() ? 'Modifier le produit' : 'Créer un produit' }}</h2>
            </div>
            <button class="close-btn" (click)="closeDrawer()" aria-label="Fermer">×</button>
          </header>

          <form [formGroup]="form" (ngSubmit)="save()" class="drawer-form">
            <div class="form-row">
              <label>Nom du produit *</label>
              <input type="text" formControlName="name" placeholder="Ex: MacBook Pro 14&quot;" />
              @if (form.get('name')?.touched && form.get('name')?.invalid) {
                <span class="err">Nom obligatoire (2-200 caractères)</span>
              }
            </div>

            <div class="form-row">
              <label>Description</label>
              <textarea formControlName="description" rows="3" placeholder="Description détaillée du produit..."></textarea>
            </div>

            <div class="form-grid">
              <div class="form-row">
                <label>Prix (MAD) *</label>
                <input type="number" formControlName="price" min="0" step="0.01" placeholder="0.00" />
              </div>

              <div class="form-row">
                <label>Catégorie *</label>
                <select formControlName="categoryId">
                  <option [value]="null">— Choisir —</option>
                  @for (c of categories; track c.id) {
                    <option [value]="c.id">{{ c.name }}</option>
                  }
                </select>
              </div>
            </div>

            <div class="form-row">
              <label>Stock initial</label>
              <input type="number" formControlName="initialStock" min="0" placeholder="0" />
              <span class="hint">Modifiable plus tard via les boutons ± de la liste.</span>
            </div>

            <div class="form-row">
              <label>URL d'image</label>
              <div class="image-row">
                <input type="text" formControlName="imageUrl" placeholder="https://... ou /uploads/products/..." />
                <button type="button" class="btn-link" (click)="generateImageFromForm()" [disabled]="!editingId() || formGenerating()">
                  @if (formGenerating()) {
                    <span class="spin"></span> Génération...
                  } @else {
                    ✦ Gemini
                  }
                </button>
              </div>
              @if (!editingId()) {
                <span class="hint">La génération Gemini est disponible après création du produit.</span>
              } @else {
                <span class="hint">Cliquez sur ✦ Gemini pour générer une image studio basée sur le nom & description.</span>
              }
              @if (form.value.imageUrl) {
                <div class="preview">
                  <img [src]="resolveImage(form.value.imageUrl)" alt="Aperçu" (error)="onImgError($event)" />
                </div>
              }
            </div>

            <div class="form-actions">
              <button type="button" class="btn-premium ghost" (click)="closeDrawer()">Annuler</button>
              <button type="submit" class="btn-premium primary" [disabled]="form.invalid || saving()">
                @if (saving()) { <span class="spin"></span> }
                {{ editingId() ? 'Enregistrer' : 'Créer le produit' }}
              </button>
            </div>
          </form>
        </aside>
      }

      <!-- ─── Confirm delete modal ─────────── -->
      @if (deleteCandidate()) {
        <div class="modal-backdrop" (click)="deleteCandidate.set(null)"></div>
        <div class="modal">
          <div class="modal-icon">⚠</div>
          <h3>Supprimer ce produit ?</h3>
          <p><strong>{{ deleteCandidate()!.name }}</strong> sera définitivement supprimé. Cette action est irréversible.</p>
          <div class="modal-actions">
            <button class="btn-premium ghost" (click)="deleteCandidate.set(null)">Annuler</button>
            <button class="btn-premium danger" (click)="doDelete()" [disabled]="deleting()">
              @if (deleting()) { <span class="spin"></span> } Supprimer
            </button>
          </div>
        </div>
      }
    </div>
  `,
  styles: [`
    :host { display: block; }

    .admin { position: relative; }

    .admin-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 2rem;
      margin-bottom: 2rem;
      flex-wrap: wrap;
    }
    .eyebrow {
      display: inline-block;
      font-size: 0.7rem;
      font-weight: 500;
      letter-spacing: 0.2em;
      color: var(--text-tertiary);
      margin-bottom: 0.7rem;
    }
    h1 {
      font-family: var(--font-display);
      font-size: clamp(1.75rem, 4vw, 2.75rem);
      font-weight: 500;
      letter-spacing: -0.02em;
      margin: 0 0 0.5rem;
      color: var(--text-primary);
    }
    .lead { font-size: 0.95rem; color: var(--text-secondary); max-width: 560px; margin: 0; }

    .stats-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      margin-bottom: 2rem;
    }
    .stat-card {
      padding: 1.25rem 1.5rem;
      background: linear-gradient(160deg, rgba(255,255,255,0.04), rgba(255,255,255,0.012));
      border: 1px solid var(--border-soft);
      border-radius: 14px;
    }
    .stat-label {
      display: block;
      font-size: 0.7rem;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--text-tertiary);
      margin-bottom: 0.4rem;
    }
    .stat-value {
      font-family: var(--font-display);
      font-size: 1.75rem;
      font-weight: 500;
      letter-spacing: -0.02em;
      color: var(--text-primary);
    }
    .stat-value.grad {
      background: linear-gradient(135deg, #22d3ee, #8b5cf6);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .stat-value.text-warn { color: #ff8a8a; }
    .stat-value.text-low { color: #fcd34d; }

    @media (max-width: 700px) { .stats-row { grid-template-columns: repeat(2, 1fr); } }

    .table-wrap {
      background: linear-gradient(160deg, rgba(255,255,255,0.025), rgba(255,255,255,0.005));
      border: 1px solid var(--border-soft);
      border-radius: 16px;
      overflow: hidden;
    }

    .admin-table {
      width: 100%;
      border-collapse: collapse;
    }
    .admin-table thead {
      background: rgba(255,255,255,0.03);
      border-bottom: 1px solid var(--border-soft);
    }
    .admin-table th {
      text-align: left;
      padding: 1rem 1.25rem;
      font-size: 0.65rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      color: var(--text-tertiary);
    }
    .admin-table th.num { text-align: right; }
    .admin-table th.img-col { width: 80px; }
    .admin-table th.stock-col { width: 160px; }
    .admin-table th.actions-col { width: 130px; }
    .admin-table td {
      padding: 1rem 1.25rem;
      border-top: 1px solid var(--border-faint);
      vertical-align: middle;
      color: var(--text-primary);
    }
    .admin-table tbody tr:hover { background: rgba(255,255,255,0.02); }

    .thumb {
      width: 56px; height: 56px;
      border-radius: 10px;
      overflow: hidden;
      background: #1d2122;
    }
    .thumb img { width: 100%; height: 100%; object-fit: cover; }

    .name-cell { display: flex; flex-direction: column; gap: 2px; max-width: 360px; }
    .name-cell strong { font-weight: 500; color: var(--text-primary); }
    .name-cell .muted {
      font-size: 0.75rem;
      color: var(--text-tertiary);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .cat-tag {
      display: inline-block;
      padding: 0.3rem 0.65rem;
      border-radius: 999px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border-soft);
      font-size: 0.7rem;
      color: var(--text-secondary);
    }

    .price-cell {
      font-family: var(--font-display);
      font-size: 1.05rem;
      font-weight: 500;
      letter-spacing: -0.01em;
      color: var(--text-primary);
    }
    .price-cell small { font-size: 0.65rem; color: var(--text-tertiary); margin-left: 0.2rem; }
    td.num { text-align: right; }

    .stock-cell {
      display: inline-flex;
      align-items: center;
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--border-soft);
      border-radius: 10px;
      overflow: hidden;
    }
    .stock-btn {
      width: 30px; height: 32px;
      background: none;
      border: none;
      color: var(--text-primary);
      cursor: pointer;
      transition: background 0.3s ease;
      font-size: 0.95rem;
    }
    .stock-btn:hover:not(:disabled) { background: rgba(255,255,255,0.06); }
    .stock-btn:disabled { opacity: 0.3; cursor: not-allowed; }
    .stock-cell input {
      width: 48px;
      text-align: center;
      background: none;
      border: none;
      color: var(--text-primary);
      font-family: var(--font-display);
      font-size: 0.875rem;
      -moz-appearance: textfield;
      padding: 0;
    }
    .stock-cell input.warn { color: #fcd34d; }
    .stock-cell input.danger { color: #ff8a8a; }
    .stock-cell input:focus { outline: none; }
    .stock-cell input::-webkit-outer-spin-button, .stock-cell input::-webkit-inner-spin-button { -webkit-appearance: none; }

    .actions { display: inline-flex; gap: 0.4rem; }
    .icon-btn {
      width: 32px; height: 32px;
      border-radius: 8px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border-soft);
      color: var(--text-secondary);
      display: grid;
      place-items: center;
      cursor: pointer;
      transition: all 0.3s ease;
    }
    .icon-btn:hover:not(:disabled) {
      background: rgba(255,255,255,0.08);
      color: var(--text-primary);
      border-color: var(--border-strong);
    }
    .icon-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .icon-btn.danger:hover {
      background: rgba(255,99,99,0.12);
      color: #ff8a8a;
      border-color: rgba(255,99,99,0.3);
    }

    .spin {
      display: inline-block;
      width: 12px; height: 12px;
      border: 1.5px solid rgba(255,255,255,0.2);
      border-top-color: currentColor;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    .empty { text-align: center; padding: 3rem 1rem; color: var(--text-tertiary); }

    .loading-wrap { padding: 3rem 0; display: grid; place-items: center; }

    /* ─── Drawer ──────────────────────── */
    .drawer-backdrop {
      position: fixed; inset: 0;
      background: rgba(0,0,0,0.5);
      backdrop-filter: blur(8px);
      z-index: 200;
      animation: fade 0.3s var(--ease-out-quart);
    }
    .drawer {
      position: fixed;
      top: 0; right: 0; bottom: 0;
      width: min(560px, 100%);
      background: linear-gradient(180deg, #1a1d1e 0%, #131616 100%);
      border-left: 1px solid var(--border-soft);
      z-index: 201;
      display: flex;
      flex-direction: column;
      animation: slide 0.4s var(--ease-out-quart);
      overflow-y: auto;
    }
    @keyframes fade { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slide { from { transform: translateX(100%); } to { transform: translateX(0); } }

    .drawer-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      padding: 2rem;
      border-bottom: 1px solid var(--border-soft);
    }
    .drawer-head h2 {
      font-family: var(--font-display);
      font-size: 1.5rem;
      font-weight: 500;
      letter-spacing: -0.02em;
      margin: 0.3rem 0 0;
      color: var(--text-primary);
    }
    .close-btn {
      width: 36px; height: 36px;
      border-radius: 50%;
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--border-soft);
      color: var(--text-primary);
      cursor: pointer;
      font-size: 1.3rem;
      line-height: 1;
    }
    .close-btn:hover { background: rgba(255,255,255,0.08); }

    .drawer-form {
      padding: 2rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    .form-row { display: flex; flex-direction: column; gap: 0.5rem; }
    .form-row label {
      font-size: 0.7rem;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--text-tertiary);
    }
    .form-row input, .form-row select, .form-row textarea {
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border-soft);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      color: var(--text-primary);
      font-family: var(--font-body);
      font-size: 0.875rem;
      transition: border-color 0.3s ease;
    }
    .form-row input:focus, .form-row select:focus, .form-row textarea:focus {
      outline: none;
      border-color: rgba(59,130,246,0.45);
      background: rgba(255,255,255,0.06);
    }
    .form-row textarea { resize: vertical; min-height: 80px; font-family: var(--font-body); }
    .form-row .hint {
      font-size: 0.75rem;
      color: var(--text-tertiary);
    }
    .form-row .err {
      font-size: 0.75rem;
      color: #ff8a8a;
    }
    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }
    .image-row {
      display: flex;
      gap: 0.5rem;
    }
    .image-row input { flex: 1; }
    .image-row button {
      padding: 0 1rem;
      border-radius: 10px;
      background: linear-gradient(135deg, rgba(34,211,238,0.12), rgba(139,92,246,0.12));
      border: 1px solid rgba(34,211,238,0.3);
      color: var(--text-primary);
      font-family: var(--font-body);
      font-size: 0.8rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.3s ease;
    }
    .image-row button:hover:not(:disabled) {
      background: linear-gradient(135deg, rgba(34,211,238,0.22), rgba(139,92,246,0.22));
      border-color: rgba(34,211,238,0.45);
    }
    .image-row button:disabled { opacity: 0.5; cursor: not-allowed; }
    .image-row .btn-link { background: linear-gradient(135deg, rgba(34,211,238,0.12), rgba(139,92,246,0.12)); }

    .preview {
      width: 100%;
      aspect-ratio: 4 / 3;
      border-radius: 12px;
      overflow: hidden;
      background: #1d2122;
      border: 1px solid var(--border-soft);
    }
    .preview img { width: 100%; height: 100%; object-fit: cover; }

    .form-actions {
      display: flex;
      gap: 0.75rem;
      justify-content: flex-end;
      margin-top: 1rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border-soft);
    }

    /* ─── Confirm modal ─────────────── */
    .modal-backdrop {
      position: fixed; inset: 0;
      background: rgba(0,0,0,0.65);
      backdrop-filter: blur(10px);
      z-index: 300;
      animation: fade 0.3s ease;
    }
    .modal {
      position: fixed;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      width: min(420px, calc(100% - 2rem));
      background: linear-gradient(180deg, #1a1d1e, #131616);
      border: 1px solid var(--border-soft);
      border-radius: 20px;
      padding: 2rem;
      z-index: 301;
      text-align: center;
      animation: pop 0.35s var(--ease-out-quart);
    }
    @keyframes pop {
      from { opacity: 0; transform: translate(-50%, -45%) scale(0.95); }
      to   { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    }
    .modal-icon {
      font-size: 2rem;
      margin-bottom: 0.75rem;
    }
    .modal h3 {
      font-family: var(--font-display);
      font-size: 1.25rem;
      margin: 0 0 0.5rem;
      color: var(--text-primary);
    }
    .modal p { color: var(--text-secondary); margin: 0 0 1.5rem; }
    .modal-actions { display: flex; gap: 0.75rem; justify-content: center; }

    .btn-premium.danger {
      background: linear-gradient(135deg, #ff6b6b, #c33);
      color: white;
      border-color: transparent;
    }
    .btn-premium.danger:hover:not(:disabled) {
      box-shadow: 0 8px 30px rgba(255,99,99,0.3);
    }

    @media (max-width: 700px) {
      .admin-head { flex-direction: column; align-items: stretch; }
      .form-grid { grid-template-columns: 1fr; }
      .admin-table { font-size: 0.85rem; }
      .admin-table th, .admin-table td { padding: 0.7rem 0.6rem; }
      .name-cell .muted { display: none; }
    }
  `]
})
export class AdminProductsComponent implements OnInit {
  private productSvc = inject(ProductService);
  private toast = inject(ToastService);
  private fb = inject(FormBuilder);

  products: Product[] = [];
  categories: Category[] = [];

  loading = signal(true);
  saving = signal(false);
  deleting = signal(false);
  savingStockId = signal<number | null>(null);
  generatingId = signal<number | null>(null);
  formGenerating = signal(false);

  drawerOpen = signal(false);
  editingId = signal<number | null>(null);
  deleteCandidate = signal<Product | null>(null);

  form: FormGroup = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(200)]],
    description: ['', [Validators.maxLength(2000)]],
    price: [0, [Validators.required, Validators.min(0.01)]],
    imageUrl: ['', [Validators.maxLength(500)]],
    categoryId: [null, [Validators.required]],
    initialStock: [0, [Validators.min(0)]]
  });

  ngOnInit(): void {
    this.productSvc.categories().subscribe((r) => (this.categories = r.data ?? []));
    this.refresh();
  }

  refresh(): void {
    this.loading.set(true);
    // Fetch up to 200 products for admin view (single page)
    this.productSvc.list({ size: 200, sort: 'newest' })
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (r) => (this.products = r.data?.content ?? []),
        error: () => (this.products = [])
      });
  }

  // ─── Stats ───────────────────────────────
  countOutOfStock(): number { return this.products.filter(p => p.stock === 0).length; }
  countLowStock(): number   { return this.products.filter(p => p.stock > 0 && p.stock < 5).length; }
  totalValue(): number      { return this.products.reduce((s, p) => s + p.price * p.stock, 0); }

  // ─── Drawer / Form ───────────────────────
  openCreate(): void {
    this.editingId.set(null);
    this.form.reset({ name: '', description: '', price: 0, imageUrl: '', categoryId: null, initialStock: 0 });
    this.drawerOpen.set(true);
  }

  openEdit(p: Product): void {
    this.editingId.set(p.id);
    this.form.reset({
      name: p.name,
      description: p.description ?? '',
      price: p.price,
      imageUrl: p.imageUrl ?? '',
      categoryId: p.categoryId,
      initialStock: p.stock
    });
    this.drawerOpen.set(true);
  }

  closeDrawer(): void {
    if (this.saving()) return;
    this.drawerOpen.set(false);
    this.editingId.set(null);
  }

  save(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    const v = this.form.value;
    const payload: AdminProductPayload = {
      name: v.name,
      description: v.description,
      price: Number(v.price),
      imageUrl: v.imageUrl,
      categoryId: Number(v.categoryId),
      initialStock: Number(v.initialStock) || 0
    };

    this.saving.set(true);
    const op = this.editingId() != null
      ? this.productSvc.update(this.editingId()!, payload)
      : this.productSvc.create(payload);

    op.pipe(finalize(() => this.saving.set(false))).subscribe({
      next: (r) => {
        this.toast.success(r.message || (this.editingId() ? 'Produit mis à jour' : 'Produit créé'));
        this.drawerOpen.set(false);
        this.editingId.set(null);
        this.refresh();
      }
    });
  }

  // ─── Delete ──────────────────────────────
  confirmDelete(p: Product): void { this.deleteCandidate.set(p); }

  doDelete(): void {
    const p = this.deleteCandidate();
    if (!p) return;
    this.deleting.set(true);
    this.productSvc.delete(p.id)
      .pipe(finalize(() => this.deleting.set(false)))
      .subscribe({
        next: () => {
          this.toast.success('Produit supprimé');
          this.deleteCandidate.set(null);
          this.refresh();
        }
      });
  }

  // ─── Stock ──────────────────────────────
  decStock(p: Product): void {
    if (p.stock > 0) this.setStockValue(p, p.stock - 1);
  }
  incStock(p: Product): void {
    this.setStockValue(p, p.stock + 1);
  }
  setStock(p: Product, raw: string): void {
    const n = Math.max(0, Number(raw) || 0);
    if (n === p.stock) return;
    this.setStockValue(p, n);
  }
  private setStockValue(p: Product, quantity: number): void {
    this.savingStockId.set(p.id);
    this.productSvc.updateStock(p.id, quantity)
      .pipe(finalize(() => this.savingStockId.set(null)))
      .subscribe({
        next: () => {
          p.stock = quantity;
          this.toast.success(`Stock mis à jour : ${quantity}`);
        }
      });
  }

  // ─── Gemini image generation ───────────
  generateImage(p: Product): void {
    this.generatingId.set(p.id);
    this.productSvc.generateImage(p.id)
      .pipe(finalize(() => this.generatingId.set(null)))
      .subscribe({
        next: (r) => {
          this.toast.success('Image générée via Gemini ✦');
          if (r.data) {
            const idx = this.products.findIndex(x => x.id === p.id);
            if (idx >= 0) this.products[idx] = { ...this.products[idx], imageUrl: r.data.imageUrl };
          }
        }
      });
  }

  generateImageFromForm(): void {
    if (!this.editingId()) return;
    this.formGenerating.set(true);
    this.productSvc.generateImage(this.editingId()!)
      .pipe(finalize(() => this.formGenerating.set(false)))
      .subscribe({
        next: (r) => {
          if (r.data?.imageUrl) {
            this.form.patchValue({ imageUrl: r.data.imageUrl });
            this.toast.success('Image générée via Gemini ✦');
          }
        }
      });
  }

  // ─── Image helpers ─────────────────────
  resolveImage(url?: string | null): string {
    if (!url) return this.placeholder();
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
    const apiBase = environment.apiUrl.replace(/\/api\/?$/, '');
    return apiBase + (url.startsWith('/') ? url : '/' + url);
  }

  onImgError(event: Event): void {
    const img = event.target as HTMLImageElement;
    img.src = this.placeholder();
  }

  private placeholder(): string {
    return 'data:image/svg+xml;utf8,' + encodeURIComponent(
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <rect width="100" height="100" fill="#1d2122"/>
        <text x="50" y="56" text-anchor="middle" fill="#6e7373" font-family="Inter" font-size="9">N/A</text>
      </svg>`
    );
  }
}
