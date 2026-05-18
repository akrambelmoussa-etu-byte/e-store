import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { CartService } from '../../core/services/cart.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <header class="topbar">
      <div class="bar-inner">
        <a class="brand" routerLink="/">
          <span class="brand-mark">⬢</span>
          <span class="brand-name">E-Store</span>
        </a>

        <nav class="links">
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: true }">Catalogue</a>
          @if (auth.isAuthenticated) {
            <a routerLink="/orders" routerLinkActive="active">Commandes</a>
            <a routerLink="/profile" routerLinkActive="active">Profil</a>
          }
          @if (auth.isAdmin) {
            <a routerLink="/admin/products" routerLinkActive="active" class="admin-link">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/></svg>
              Admin
            </a>
          }
        </nav>

        <div class="actions">
          @if (auth.isAuthenticated) {
            <a routerLink="/cart" class="icon-link" routerLinkActive="active" aria-label="Panier">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/></svg>
              @if (cartSvc.itemCount() > 0) {
                <span class="cart-badge">{{ cartSvc.itemCount() }}</span>
              }
            </a>
            <span class="user-name">{{ auth.currentUser?.firstName }}</span>
            <button class="btn-premium ghost btn-sm" (click)="auth.logout()">Déconnexion</button>
          } @else {
            <a class="btn-premium ghost btn-sm" routerLink="/login">Connexion</a>
            <a class="btn-premium primary btn-sm" routerLink="/register">Inscription</a>
          }
        </div>
      </div>
    </header>
  `,
  styles: [`
    .topbar {
      position: sticky; top: 0; z-index: 50;
      backdrop-filter: blur(14px);
      background: rgba(14, 16, 18, 0.78);
      border-bottom: 1px solid var(--border-soft);
    }
    .bar-inner {
      max-width: 1340px;
      margin: 0 auto;
      padding: 0.85rem 1.5rem;
      display: flex; align-items: center; gap: 1.6rem;
    }

    .brand {
      display: flex; align-items: center; gap: 0.5rem;
      text-decoration: none;
      font-family: var(--font-display);
      font-weight: 700;
    }
    .brand-mark {
      width: 32px; height: 32px;
      display: inline-flex; align-items: center; justify-content: center;
      background: var(--accent-grad);
      color: var(--text-inverse);
      border-radius: 8px;
      font-size: 1.1rem;
    }
    .brand-name { color: var(--text-primary); font-size: 1.1rem; letter-spacing: -0.02em; }

    .links {
      display: flex; gap: 1.4rem; align-items: center;
      margin-right: auto;
    }
    .links a {
      color: var(--text-secondary);
      text-decoration: none;
      font-size: 0.9rem;
      position: relative;
      padding: 0.35rem 0;
      transition: color 0.2s ease;
    }
    .links a:hover { color: var(--text-primary); }
    .links a.active {
      color: var(--text-primary);
    }
    .links a.active::after {
      content: '';
      position: absolute; left: 0; right: 0; bottom: -2px;
      height: 2px; background: var(--accent-grad);
      border-radius: 2px;
    }

    .admin-link {
      display: inline-flex; align-items: center; gap: 0.35rem;
      padding: 0.3rem 0.7rem !important;
      background: rgba(139, 92, 246, 0.12);
      border: 1px solid rgba(139, 92, 246, 0.32);
      border-radius: 999px;
      color: #c4b5fd !important;
    }
    .admin-link:hover { background: rgba(139, 92, 246, 0.2); }

    .actions { display: flex; align-items: center; gap: 0.7rem; }
    .btn-sm { padding: 0.45rem 0.85rem !important; font-size: 0.8rem; }
    .user-name { color: var(--text-secondary); font-size: 0.85rem; }

    .icon-link {
      position: relative;
      width: 38px; height: 38px;
      display: inline-flex; align-items: center; justify-content: center;
      color: var(--text-secondary);
      background: var(--surface);
      border: 1px solid var(--border-soft);
      border-radius: 50%;
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .icon-link:hover, .icon-link.active { color: var(--text-primary); background: var(--surface-hover); }
    .cart-badge {
      position: absolute; top: -4px; right: -4px;
      min-width: 18px; height: 18px;
      padding: 0 5px;
      display: inline-flex; align-items: center; justify-content: center;
      background: var(--accent-grad); color: var(--text-inverse);
      border-radius: 999px;
      font-size: 0.7rem; font-weight: 700;
    }

    @media (max-width: 760px) {
      .bar-inner { gap: 0.8rem; flex-wrap: wrap; }
      .links { order: 3; width: 100%; overflow-x: auto; padding-top: 0.5rem; }
      .user-name { display: none; }
    }
  `]
})
export class HeaderComponent {
  auth = inject(AuthService);
  cartSvc = inject(CartService);
}
