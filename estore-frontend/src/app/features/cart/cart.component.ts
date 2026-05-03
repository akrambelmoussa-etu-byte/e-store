import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CartService } from '../../core/services/cart.service';
import { OrderService } from '../../core/services/order.service';
import { ToastService } from '../../core/services/toast.service';
import { LoaderComponent } from '../../shared/components/loader.component';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LoaderComponent],
  template: `
    <h2 class="section-title mb-4">Mon panier</h2>

    @if (loading) {
      <app-loader />
    } @else if (!cartSvc.cart() || cartSvc.cart()!.items.length === 0) {
      <div class="alert alert-info">
        Votre panier est vide. <a routerLink="/">Continuer mes achats</a>
      </div>
    } @else {
      <div class="card shadow-sm">
        <div class="table-responsive">
          <table class="table mb-0 align-middle">
            <thead class="table-light">
              <tr>
                <th>Produit</th>
                <th>Prix unitaire</th>
                <th style="width: 130px">Quantité</th>
                <th>Sous-total</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              @for (item of cartSvc.cart()!.items; track item.id) {
                <tr>
                  <td>
                    <div class="d-flex align-items-center gap-2">
                      @if (item.imageUrl) {
                        <img [src]="item.imageUrl" width="50" height="50" style="object-fit: cover" />
                      }
                      <span>{{ item.productName }}</span>
                    </div>
                  </td>
                  <td>{{ item.unitPrice | number:'1.2-2' }} MAD</td>
                  <td>
                    <input
                      type="number"
                      min="1"
                      class="form-control form-control-sm"
                      [ngModel]="item.quantity"
                      (change)="update(item.id, $any($event.target).value)"
                    />
                  </td>
                  <td><strong>{{ item.subtotal | number:'1.2-2' }} MAD</strong></td>
                  <td>
                    <button class="btn btn-sm btn-outline-danger" (click)="remove(item.id)">×</button>
                  </td>
                </tr>
              }
            </tbody>
            <tfoot>
              <tr>
                <td colspan="3" class="text-end"><strong>Total</strong></td>
                <td colspan="2"><strong class="text-primary">{{ cartSvc.cart()!.total | number:'1.2-2' }} MAD</strong></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      <div class="d-flex justify-content-between mt-4">
        <button class="btn btn-outline-secondary" (click)="clearCart()">Vider le panier</button>
        <button class="btn btn-success" [disabled]="placing" (click)="checkout()">
          @if (placing) {
            <span class="spinner-border spinner-border-sm me-2"></span>
          }
          Valider la commande
        </button>
      </div>
    }
  `
})
export class CartComponent implements OnInit {
  cartSvc = inject(CartService);
  private orderSvc = inject(OrderService);
  private toast = inject(ToastService);
  private router = inject(Router);

  loading = true;
  placing = false;

  ngOnInit(): void {
    this.cartSvc.get().subscribe({
      next: () => (this.loading = false),
      error: () => (this.loading = false)
    });
  }

  update(itemId: number, qty: string): void {
    const q = Number(qty);
    if (q < 1) return;
    this.cartSvc.updateItem(itemId, q).subscribe({ next: () => this.toast.success('Quantité mise à jour') });
  }

  remove(itemId: number): void {
    this.cartSvc.remove(itemId).subscribe({ next: () => this.toast.success('Article retiré') });
  }

  clearCart(): void {
    this.cartSvc.clear().subscribe({ next: () => this.toast.info('Panier vidé') });
  }

  checkout(): void {
    this.placing = true;
    this.orderSvc.checkout().subscribe({
      next: (r) => {
        this.toast.success('Commande #' + r.data?.id + ' confirmée !');
        this.cartSvc.get().subscribe();
        this.router.navigate(['/orders']);
      },
      error: () => (this.placing = false),
      complete: () => (this.placing = false)
    });
  }
}
