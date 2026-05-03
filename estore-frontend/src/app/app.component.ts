import { Component, OnInit, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './shared/components/header.component';
import { FooterComponent } from './shared/components/footer.component';
import { ToastComponent } from './shared/components/toast.component';
import { AuthService } from './core/services/auth.service';
import { CartService } from './core/services/cart.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent, FooterComponent, ToastComponent],
  template: `
    <app-header />
    <app-toast />
    <main class="container py-4">
      <router-outlet />
    </main>
    <app-footer />
  `
})
export class AppComponent implements OnInit {
  private auth = inject(AuthService);
  private cartSvc = inject(CartService);

  ngOnInit(): void {
    if (this.auth.isAuthenticated) {
      this.cartSvc.get().subscribe({ error: () => {} });
    }
  }
}
