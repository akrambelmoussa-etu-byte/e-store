import { Injectable, inject } from '@angular/core';
import { Observable, of, throwError, delay, mergeMap } from 'rxjs';
import { OrderService } from './order.service';
import { ApiResponse } from '../models/api-response.model';
import { Order } from '../models/order.model';

/**
 * Card brands we recognise for visual badge + sane CVV length.
 * Detection uses the standard issuer-prefix table; replace with a vendor SDK
 * if/when real card processing is added.
 */
export type CardBrand = 'visa' | 'mastercard' | 'amex' | 'discover' | 'maestro' | 'unknown';

export interface CardData {
  number: string;        // raw digits only
  name: string;
  expiryMonth: string;   // "MM"
  expiryYear: string;    // "YY"
  cvv: string;
  saveCard?: boolean;
}

export interface PaymentResult {
  status: 'succeeded' | 'failed';
  transactionId: string;
  brand: CardBrand;
  last4: string;
  amount: number;
  order?: Order;
  reason?: string;
}

@Injectable({ providedIn: 'root' })
export class PaymentService {
  private orderSvc = inject(OrderService);

  /**
   * Runs a 3-step simulation (validation → tokenisation → authorisation)
   * before delegating to the real checkout endpoint that turns the cart
   * into an order. Total time ~2.4s — long enough to feel processed,
   * short enough not to annoy.
   */
  charge(card: CardData, amount: number): Observable<PaymentResult> {
    // 1. Synchronous validation
    const validation = this.validate(card);
    if (validation) {
      return throwError(() => ({
        status: 'failed' as const,
        transactionId: this.txnId(),
        brand: this.detectBrand(card.number),
        last4: card.number.slice(-4),
        amount,
        reason: validation
      }));
    }

    // 2. Simulated network latency (auth call to fake gateway)
    return of(null).pipe(
      delay(1400),
      mergeMap(() => {
        // Specific test cards
        const digits = card.number.replace(/\D+/g, '');
        if (digits === '4000000000000002') {
          // "card declined" test card
          return throwError(() => ({
            status: 'failed' as const,
            transactionId: this.txnId(),
            brand: this.detectBrand(digits),
            last4: digits.slice(-4),
            amount,
            reason: 'Carte refusée par la banque émettrice'
          }));
        }

        // 3. Confirm order on the real backend
        return this.orderSvc.checkout().pipe(
          mergeMap((res: ApiResponse<Order>) =>
            of<PaymentResult>({
              status: 'succeeded',
              transactionId: this.txnId(),
              brand: this.detectBrand(digits),
              last4: digits.slice(-4),
              amount,
              order: res.data!
            })
          )
        );
      })
    );
  }

  // ----------- Validation helpers -----------

  /** @returns null when card is valid; an error message otherwise. */
  validate(card: CardData): string | null {
    const digits = card.number.replace(/\D+/g, '');
    if (digits.length < 13 || digits.length > 19) return 'Numéro de carte invalide (longueur)';
    if (!this.luhn(digits)) return 'Numéro de carte invalide (Luhn)';
    if (!card.name || card.name.trim().length < 2) return 'Nom du porteur requis';

    const mm = parseInt(card.expiryMonth, 10);
    const yy = parseInt(card.expiryYear, 10);
    if (isNaN(mm) || mm < 1 || mm > 12) return 'Mois d\'expiration invalide';
    if (isNaN(yy)) return 'Année d\'expiration invalide';

    const now = new Date();
    const exp = new Date(2000 + yy, mm, 0, 23, 59, 59);
    if (exp < now) return 'Carte expirée';

    const brand = this.detectBrand(digits);
    const expectedCvv = brand === 'amex' ? 4 : 3;
    if (!/^\d+$/.test(card.cvv) || card.cvv.length !== expectedCvv) {
      return `CVV invalide (${expectedCvv} chiffres attendus)`;
    }

    return null;
  }

  /** Luhn checksum (mod-10). */
  luhn(digits: string): boolean {
    let sum = 0;
    let alt = false;
    for (let i = digits.length - 1; i >= 0; i--) {
      let n = parseInt(digits.charAt(i), 10);
      if (alt) {
        n *= 2;
        if (n > 9) n -= 9;
      }
      sum += n;
      alt = !alt;
    }
    return sum % 10 === 0;
  }

  detectBrand(rawNumber: string): CardBrand {
    const n = rawNumber.replace(/\D+/g, '');
    if (/^4/.test(n)) return 'visa';
    if (/^(5[1-5]|2[2-7])/.test(n)) return 'mastercard';
    if (/^3[47]/.test(n)) return 'amex';
    if (/^6(011|5)/.test(n)) return 'discover';
    if (/^(5018|5020|5038|6304|6759|6761|6763)/.test(n)) return 'maestro';
    return 'unknown';
  }

  /** Auto-format card number as user types: groups of 4 (or 4-6-5 for Amex). */
  formatNumber(input: string): string {
    const digits = input.replace(/\D+/g, '').slice(0, 19);
    const brand = this.detectBrand(digits);
    if (brand === 'amex') {
      return digits.replace(/^(\d{0,4})(\d{0,6})(\d{0,5}).*/, (_, a, b, c) =>
        [a, b, c].filter(Boolean).join(' ')
      );
    }
    return digits.replace(/(.{4})/g, '$1 ').trim();
  }

  formatExpiry(input: string): string {
    const digits = input.replace(/\D+/g, '').slice(0, 4);
    if (digits.length <= 2) return digits;
    return digits.slice(0, 2) + '/' + digits.slice(2);
  }

  private txnId(): string {
    const r = Math.random().toString(36).slice(2, 10).toUpperCase();
    return 'TXN-' + Date.now().toString(36).toUpperCase() + '-' + r;
  }
}
