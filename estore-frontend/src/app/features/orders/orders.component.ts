import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OrderService } from '../../core/services/order.service';
import { Order } from '../../core/models/order.model';
import { LoaderComponent } from '../../shared/components/loader.component';

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [CommonModule, LoaderComponent],
  template: `
    <h2 class="section-title mb-4">Mes commandes</h2>

    @if (loading) {
      <app-loader />
    } @else if (orders.length === 0) {
      <div class="alert alert-info">Vous n'avez encore passé aucune commande.</div>
    } @else {
      <div class="accordion" id="ordersAcc">
        @for (o of orders; track o.id) {
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button
                class="accordion-button collapsed"
                type="button"
                (click)="toggle(o.id)"
                [attr.aria-expanded]="expanded === o.id"
              >
                <div class="d-flex justify-content-between w-100 me-3">
                  <span>
                    <strong>Commande #{{ o.id }}</strong>
                    <span class="text-muted ms-2">{{ o.orderDate | date:'medium' }}</span>
                  </span>
                  <span>
                    <span class="badge bg-{{ statusClass(o.status) }} me-2">{{ statusLabel(o.status) }}</span>
                    <strong>{{ o.totalAmount | number:'1.2-2' }} MAD</strong>
                  </span>
                </div>
              </button>
            </h2>
            <div class="accordion-collapse collapse" [class.show]="expanded === o.id">
              <div class="accordion-body">
                <table class="table table-sm">
                  <thead>
                    <tr>
                      <th>Produit</th>
                      <th>Qté</th>
                      <th>Prix unitaire</th>
                      <th>Sous-total</th>
                    </tr>
                  </thead>
                  <tbody>
                    @for (item of o.items; track item.id) {
                      <tr>
                        <td>{{ item.productName }}</td>
                        <td>{{ item.quantity }}</td>
                        <td>{{ item.unitPrice | number:'1.2-2' }} MAD</td>
                        <td><strong>{{ item.subtotal | number:'1.2-2' }} MAD</strong></td>
                      </tr>
                    }
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        }
      </div>
    }
  `
})
export class OrdersComponent implements OnInit {
  private orderSvc = inject(OrderService);
  orders: Order[] = [];
  loading = true;
  expanded: number | null = null;

  ngOnInit(): void {
    this.orderSvc.list().subscribe({
      next: (r) => {
        this.orders = r.data ?? [];
        this.loading = false;
      },
      error: () => (this.loading = false)
    });
  }

  toggle(id: number): void {
    this.expanded = this.expanded === id ? null : id;
  }

  statusClass(s: string): string {
    return s === 'CONFIRMED' ? 'success' : s === 'CANCELLED' ? 'danger' : 'warning';
  }

  statusLabel(s: string): string {
    return s === 'CONFIRMED' ? 'Confirmée' : s === 'CANCELLED' ? 'Annulée' : 'En attente';
  }
}
