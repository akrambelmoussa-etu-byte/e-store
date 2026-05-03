import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ApiResponse } from '../models/api-response.model';
import { Cart } from '../models/cart.model';

@Injectable({ providedIn: 'root' })
export class CartService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/cart`;

  readonly cart = signal<Cart | null>(null);
  readonly itemCount = signal<number>(0);

  get(): Observable<ApiResponse<Cart>> {
    return this.http.get<ApiResponse<Cart>>(this.base).pipe(tap((r) => this.update(r.data)));
  }

  add(productId: number, quantity: number): Observable<ApiResponse<Cart>> {
    return this.http
      .post<ApiResponse<Cart>>(`${this.base}/add`, { productId, quantity })
      .pipe(tap((r) => this.update(r.data)));
  }

  updateItem(itemId: number, quantity: number): Observable<ApiResponse<Cart>> {
    return this.http
      .put<ApiResponse<Cart>>(`${this.base}/update`, { itemId, quantity })
      .pipe(tap((r) => this.update(r.data)));
  }

  remove(itemId: number): Observable<ApiResponse<Cart>> {
    return this.http
      .delete<ApiResponse<Cart>>(`${this.base}/remove/${itemId}`)
      .pipe(tap((r) => this.update(r.data)));
  }

  clear(): Observable<ApiResponse<Cart>> {
    return this.http.delete<ApiResponse<Cart>>(`${this.base}/clear`).pipe(tap((r) => this.update(r.data)));
  }

  private update(cart: Cart | undefined): void {
    if (!cart) return;
    this.cart.set(cart);
    this.itemCount.set(cart.itemCount);
  }
}
