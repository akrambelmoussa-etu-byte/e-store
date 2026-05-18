import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ApiResponse } from '../models/api-response.model';
import { Category, PageResponse, Product } from '../models/product.model';

/** Clés acceptées par le backend pour trier le catalogue. */
export type ProductSort = 'newest' | 'oldest' | 'price_asc' | 'price_desc' | 'name_asc' | 'name_desc';

/** Options de requête de la liste produit — toutes optionnelles. */
export interface ProductListOpts {
  categoryId?: number | null;
  q?: string;
  page?: number;
  size?: number;
  minPrice?: number | null;
  maxPrice?: number | null;
  inStockOnly?: boolean;
  sort?: ProductSort;
}

/** Payload partagé entre create() et update() depuis l'admin. */
export interface AdminProductPayload {
  name: string;
  description?: string;
  price: number;
  imageUrl?: string;
  categoryId: number;
  initialStock?: number;
}

@Injectable({ providedIn: 'root' })
export class ProductService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  list(opts: ProductListOpts = {}): Observable<ApiResponse<PageResponse<Product>>> {
    let params = new HttpParams();
    if (opts.categoryId != null) params = params.set('categoryId', opts.categoryId);
    if (opts.q) params = params.set('q', opts.q);
    if (opts.page != null) params = params.set('page', opts.page);
    if (opts.size != null) params = params.set('size', opts.size);
    if (opts.minPrice != null) params = params.set('minPrice', opts.minPrice);
    if (opts.maxPrice != null) params = params.set('maxPrice', opts.maxPrice);
    if (opts.inStockOnly) params = params.set('inStockOnly', true);
    if (opts.sort) params = params.set('sort', opts.sort);
    return this.http.get<ApiResponse<PageResponse<Product>>>(`${this.base}/products`, { params });
  }

  getById(id: number): Observable<ApiResponse<Product>> {
    return this.http.get<ApiResponse<Product>>(`${this.base}/products/${id}`);
  }

  categories(): Observable<ApiResponse<Category[]>> {
    return this.http.get<ApiResponse<Category[]>>(`${this.base}/categories`);
  }

  // ───────────────── Admin ─────────────────

  create(payload: AdminProductPayload): Observable<ApiResponse<Product>> {
    return this.http.post<ApiResponse<Product>>(`${this.base}/products`, payload);
  }

  update(id: number, payload: AdminProductPayload): Observable<ApiResponse<Product>> {
    return this.http.put<ApiResponse<Product>>(`${this.base}/products/${id}`, payload);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/products/${id}`);
  }

  /** Met à jour le stock via /api/inventory/{productId}. */
  updateStock(productId: number, quantity: number): Observable<ApiResponse<unknown>> {
    return this.http.put<ApiResponse<unknown>>(`${this.base}/inventory/${productId}`, { quantity });
  }

  /** Déclenche une génération d'image studio par Gemini Nano Banana. */
  generateImage(productId: number, customPrompt?: string): Observable<ApiResponse<Product>> {
    const body: Record<string, string> = {};
    if (customPrompt && customPrompt.trim()) body['prompt'] = customPrompt.trim();
    return this.http.post<ApiResponse<Product>>(
      `${this.base}/products/${productId}/generate-image`,
      body
    );
  }
}
