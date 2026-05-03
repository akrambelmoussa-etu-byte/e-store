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
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container">
        <a class="navbar-brand fw-bold" routerLink="/">
          <span>🛒 E-Store</span>
        </a>
        <button class="navbar-toggler" type="button" (click)="open = !open">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" [class.show]="open">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <a class="nav-link" routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: true }">
                Catalogue
              </a>
            </li>
            @if (auth.isAuthenticated) {
              <li class="nav-item">
                <a class="nav-link" routerLink="/orders" routerLinkActive="active">Mes commandes</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" routerLink="/profile" routerLinkActive="active">Mon profil</a>
              </li>
            }
          </ul>
          <ul class="navbar-nav">
            @if (auth.isAuthenticated) {
              <li class="nav-item">
                <a class="nav-link position-relative" routerLink="/cart" routerLinkActive="active">
                  Panier
                  @if (cartSvc.itemCount() > 0) {
                    <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                      {{ cartSvc.itemCount() }}
                    </span>
                  }
                </a>
              </li>
              <li class="nav-item">
                <span class="nav-link text-light">
                  Bonjour, <strong>{{ auth.currentUser?.firstName }}</strong>
                </span>
              </li>
              <li class="nav-item">
                <button class="btn btn-outline-light btn-sm ms-2" (click)="auth.logout()">Déconnexion</button>
              </li>
            } @else {
              <li class="nav-item">
                <a class="nav-link" routerLink="/login">Connexion</a>
              </li>
              <li class="nav-item">
                <a class="btn btn-light btn-sm ms-2" routerLink="/register">Inscription</a>
              </li>
            }
          </ul>
        </div>
      </div>
    </nav>
  `
})
export class HeaderComponent {
  auth = inject(AuthService);
  cartSvc = inject(CartService);
  open = false;
}
