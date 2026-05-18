import { Component, OnInit, OnDestroy, inject, signal, computed, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';
import { gsap } from 'gsap';
import { CartService } from '../../core/services/cart.service';
import { PaymentService, CardBrand, CardData } from '../../core/services/payment.service';
import { ToastService } from '../../core/services/toast.service';
import { AuthService } from '../../core/services/auth.service';
import { Order } from '../../core/models/order.model';
import { LoaderComponent } from '../../shared/components/loader.component';

type Step = 'review' | 'pay' | 'processing' | 'success' | 'failed';

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink, LoaderComponent],
  template: `
    <div class="checkout" #root>
      <!-- Stepper -->
      <nav class="stepper" aria-label="Étapes de paiement">
        <span class="step" [class.active]="step() === 'review'" [class.done]="afterReview()">
          <span class="num">1</span>
          <span class="lbl">Panier</span>
        </span>
        <span class="line" [class.fill]="afterReview()"></span>
        <span class="step" [class.active]="step() === 'pay' || step() === 'processing'" [class.done]="step() === 'success'">
          <span class="num">2</span>
          <span class="lbl">Paiement</span>
        </span>
        <span class="line" [class.fill]="step() === 'success'"></span>
        <span class="step" [class.active]="step() === 'success'">
          <span class="num">3</span>
          <span class="lbl">Confirmation</span>
        </span>
      </nav>

      <!-- ─── Step 1: review cart ─────────── -->
      @if (step() === 'review') {
        @if (loading()) {
          <div class="loading-wrap"><app-loader message="Préparation du panier..." /></div>
        } @else if (!hasItems()) {
          <div class="empty-checkout">
            <div class="empty-icon">🛒</div>
            <h2>Votre panier est vide</h2>
            <p>Ajoutez des produits avant de procéder au paiement.</p>
            <a class="btn-premium primary" routerLink="/">Parcourir le catalogue</a>
          </div>
        } @else {
          <div class="review-layout">
            <section class="items-block">
              <header class="block-head">
                <span class="eyebrow">· VOTRE COMMANDE</span>
                <h2>{{ cartSvc.itemCount() }} article{{ cartSvc.itemCount() > 1 ? 's' : '' }}</h2>
              </header>

              <div class="items">
                @for (item of cartSvc.cart()?.items ?? []; track item.id) {
                  <article class="item">
                    @if (item.imageUrl) {
                      <img [src]="item.imageUrl" [alt]="item.productName" />
                    } @else {
                      <div class="ph"></div>
                    }
                    <div class="item-info">
                      <strong>{{ item.productName }}</strong>
                      <span class="muted">{{ item.unitPrice | number:'1.0-0' }} MAD × {{ item.quantity }}</span>
                    </div>
                    <span class="subtotal">{{ item.subtotal | number:'1.0-0' }} MAD</span>
                  </article>
                }
              </div>
            </section>

            <aside class="summary">
              <header class="block-head">
                <span class="eyebrow">· RÉCAPITULATIF</span>
                <h2>À payer</h2>
              </header>

              <dl class="lines">
                <div>
                  <dt>Sous-total</dt>
                  <dd>{{ subtotal() | number:'1.0-0' }} MAD</dd>
                </div>
                <div>
                  <dt>Livraison</dt>
                  <dd>{{ shipping() === 0 ? 'Offerte' : (shipping() | number:'1.0-0') + ' MAD' }}</dd>
                </div>
                <div>
                  <dt>TVA (20%)</dt>
                  <dd>{{ tax() | number:'1.0-0' }} MAD</dd>
                </div>
                <div class="total-line">
                  <dt>Total TTC</dt>
                  <dd class="grad">{{ total() | number:'1.0-0' }} MAD</dd>
                </div>
              </dl>

              <button class="btn-premium primary block" (click)="goToPay()">
                Procéder au paiement
                <span class="arrow">→</span>
              </button>
              <a class="back" routerLink="/cart">← Modifier le panier</a>
            </aside>
          </div>
        }
      }

      <!-- ─── Step 2: pay with card ─────────── -->
      @if (step() === 'pay' || step() === 'processing') {
        <div class="pay-layout">
          <section class="card-block">
            <header class="block-head">
              <span class="eyebrow">· INFORMATIONS DE PAIEMENT</span>
              <h2>Vos détails de carte</h2>
              <p class="hint">Aucune transaction réelle n'est effectuée. Carte de test : <code>4242 4242 4242 4242</code></p>
            </header>

            <!-- Card preview -->
            <div class="card-preview" #preview [class.flipped]="cvvFocused()">
              <div class="card-face front" [attr.data-brand]="brand()">
                <div class="chip"></div>
                <div class="brand-mark">{{ brandLabel() }}</div>
                <div class="card-number">{{ cardNumberMasked() }}</div>
                <div class="card-row">
                  <div>
                    <span class="lbl">TITULAIRE</span>
                    <span class="val">{{ form.value.name || 'NOM PRÉNOM' }}</span>
                  </div>
                  <div>
                    <span class="lbl">EXPIRE</span>
                    <span class="val">{{ form.value.expiryMonth || 'MM' }}/{{ form.value.expiryYear || 'YY' }}</span>
                  </div>
                </div>
              </div>
              <div class="card-face back">
                <div class="strip"></div>
                <div class="cvv-box">
                  <span class="cvv-lbl">CVV</span>
                  <span class="cvv-val">{{ form.value.cvv || '•••' }}</span>
                </div>
              </div>
            </div>

            <form [formGroup]="form" (ngSubmit)="pay()" class="card-form">
              <div class="form-row">
                <label>Numéro de carte</label>
                <div class="card-input-wrap">
                  <input
                    type="text"
                    formControlName="number"
                    placeholder="1234 5678 9012 3456"
                    autocomplete="cc-number"
                    inputmode="numeric"
                    (input)="onNumberInput($event)"
                    maxlength="23"
                  />
                  <span class="brand-icon">{{ brandLabel() }}</span>
                </div>
              </div>

              <div class="form-row">
                <label>Nom du titulaire</label>
                <input type="text" formControlName="name" placeholder="Akram Belmoussa" autocomplete="cc-name" (input)="toUpper($event)" />
              </div>

              <div class="form-grid">
                <div class="form-row">
                  <label>Mois</label>
                  <input type="text" formControlName="expiryMonth" placeholder="MM" maxlength="2" inputmode="numeric" autocomplete="cc-exp-month" />
                </div>
                <div class="form-row">
                  <label>Année</label>
                  <input type="text" formControlName="expiryYear" placeholder="YY" maxlength="2" inputmode="numeric" autocomplete="cc-exp-year" />
                </div>
                <div class="form-row">
                  <label>CVV</label>
                  <input
                    type="text"
                    formControlName="cvv"
                    [maxlength]="brand() === 'amex' ? 4 : 3"
                    placeholder="123"
                    inputmode="numeric"
                    autocomplete="cc-csc"
                    (focus)="cvvFocused.set(true)"
                    (blur)="cvvFocused.set(false)"
                  />
                </div>
              </div>

              @if (paymentError()) {
                <div class="alert-err">
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="7" cy="7" r="6"/>
                    <path d="M7 4V8M7 10V10.5" stroke-linecap="round"/>
                  </svg>
                  <span>{{ paymentError() }}</span>
                </div>
              }

              <div class="security-row">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="6" width="8" height="6" rx="1"/>
                  <path d="M5 6V4C5 2.9 5.9 2 7 2C8.1 2 9 2.9 9 4V6" stroke-linecap="round"/>
                </svg>
                Connexion chiffrée · données non stockées · simulation pédagogique
              </div>

              <button class="btn-premium primary block" type="submit" [disabled]="step() === 'processing'">
                @if (step() === 'processing') {
                  <span class="spin"></span>
                  <span>Traitement en cours...</span>
                } @else {
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.6">
                    <rect x="1" y="3" width="12" height="8" rx="1"/>
                    <path d="M1 6H13" stroke-linecap="round"/>
                  </svg>
                  <span>Payer {{ total() | number:'1.0-0' }} MAD</span>
                }
              </button>
              <button type="button" class="back-btn" (click)="step.set('review')" [disabled]="step() === 'processing'">
                ← Revenir au panier
              </button>
            </form>
          </section>

          <aside class="summary side">
            <header class="block-head">
              <span class="eyebrow">· RÉCAPITULATIF</span>
              <h2>{{ total() | number:'1.0-0' }} MAD</h2>
            </header>
            <ul class="items-mini">
              @for (item of cartSvc.cart()?.items ?? []; track item.id) {
                <li>
                  <span>{{ item.quantity }}×</span>
                  <span class="name">{{ item.productName }}</span>
                  <span>{{ item.subtotal | number:'1.0-0' }}</span>
                </li>
              }
            </ul>
            <dl class="lines">
              <div><dt>Sous-total</dt><dd>{{ subtotal() | number:'1.0-0' }} MAD</dd></div>
              <div><dt>Livraison</dt><dd>{{ shipping() === 0 ? 'Offerte' : (shipping() | number:'1.0-0') + ' MAD' }}</dd></div>
              <div><dt>TVA</dt><dd>{{ tax() | number:'1.0-0' }} MAD</dd></div>
              <div class="total-line"><dt>Total</dt><dd class="grad">{{ total() | number:'1.0-0' }} MAD</dd></div>
            </dl>
          </aside>
        </div>
      }

      <!-- ─── Step 3: success ───────────────── -->
      @if (step() === 'success' && lastOrder()) {
        <div class="result success" #result>
          <div class="success-anim">
            <svg viewBox="0 0 80 80" width="80" height="80" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="40" cy="40" r="36" stroke="url(#g)" stroke-dasharray="226" stroke-dashoffset="226" class="ring"/>
              <path d="M22 40L36 54L60 28" stroke="url(#g)" stroke-dasharray="60" stroke-dashoffset="60" class="check"/>
              <defs>
                <linearGradient id="g" x1="0" y1="0" x2="80" y2="80">
                  <stop stop-color="#22d3ee"/>
                  <stop offset="0.5" stop-color="#3b82f6"/>
                  <stop offset="1" stop-color="#8b5cf6"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h2>Paiement confirmé</h2>
          <p class="muted">Votre commande <strong class="grad">#{{ lastOrder()!.id }}</strong> a été passée avec succès.</p>

          <div class="receipt">
            <div class="r-row"><dt>Transaction</dt><dd>{{ lastTxnId() }}</dd></div>
            <div class="r-row"><dt>Carte</dt><dd>{{ brandLabel() }} •••• {{ lastLast4() }}</dd></div>
            <div class="r-row"><dt>Montant débité</dt><dd>{{ total() | number:'1.0-0' }} MAD</dd></div>
            <div class="r-row"><dt>Statut</dt><dd class="grad">{{ lastOrder()!.status }}</dd></div>
            <div class="r-row"><dt>Articles</dt><dd>{{ lastOrder()!.items.length }}</dd></div>
          </div>

          <div class="success-actions">
            <a class="btn-premium primary" routerLink="/orders">Voir mes commandes</a>
            <a class="btn-premium ghost" routerLink="/">Continuer mes achats</a>
          </div>
        </div>
      }

      <!-- ─── Step failed ──────────────────── -->
      @if (step() === 'failed') {
        <div class="result failed">
          <div class="fail-icon">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none" stroke="#ff6b6b" stroke-width="3" stroke-linecap="round">
              <circle cx="32" cy="32" r="28"/>
              <path d="M22 22L42 42M42 22L22 42"/>
            </svg>
          </div>
          <h2>Paiement refusé</h2>
          <p class="muted">{{ paymentError() || 'Une erreur est survenue lors du traitement.' }}</p>
          <div class="success-actions">
            <button class="btn-premium primary" (click)="retryPayment()">Réessayer</button>
            <a class="btn-premium ghost" routerLink="/cart">Modifier le panier</a>
          </div>
        </div>
      }
    </div>
  `,
  styles: [`
    :host { display: block; }

    .checkout { max-width: 1100px; margin: 0 auto; }

    /* ─── Stepper ──────────────────────────── */
    .stepper {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      margin-bottom: 3rem;
      flex-wrap: wrap;
    }
    .step {
      display: inline-flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.6rem 1rem;
      border-radius: 999px;
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--border-soft);
      color: var(--text-tertiary);
      font-size: 0.825rem;
      transition: all 0.4s ease;
    }
    .step.active {
      background: linear-gradient(135deg, rgba(34,211,238,0.12), rgba(139,92,246,0.12));
      border-color: rgba(34,211,238,0.3);
      color: var(--text-primary);
    }
    .step.done { background: rgba(34,211,238,0.06); border-color: rgba(34,211,238,0.2); color: var(--grad-cyan); }
    .step .num {
      width: 22px; height: 22px;
      border-radius: 50%;
      background: rgba(255,255,255,0.06);
      display: grid; place-items: center;
      font-size: 0.75rem;
      font-weight: 500;
    }
    .step.active .num, .step.done .num {
      background: linear-gradient(135deg, #22d3ee, #8b5cf6);
      color: #0b0c0c;
      font-weight: 600;
    }
    .line {
      flex: 1;
      max-width: 60px;
      height: 1px;
      background: var(--border-soft);
      transition: background 0.4s ease;
    }
    .line.fill { background: linear-gradient(90deg, #22d3ee, #8b5cf6); }

    /* ─── Block heads ─────────────────────── */
    .block-head { margin-bottom: 1.5rem; }
    .eyebrow {
      display: inline-block;
      font-size: 0.7rem;
      font-weight: 500;
      letter-spacing: 0.18em;
      color: var(--text-tertiary);
      margin-bottom: 0.5rem;
    }
    .block-head h2 {
      font-family: var(--font-display);
      font-size: 1.6rem;
      font-weight: 500;
      letter-spacing: -0.02em;
      margin: 0;
      color: var(--text-primary);
    }
    .block-head .hint {
      font-size: 0.825rem;
      color: var(--text-secondary);
      margin: 0.7rem 0 0;
    }
    .block-head code {
      background: rgba(255,255,255,0.06);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'Inter', monospace;
      font-size: 0.8rem;
    }

    /* ─── Step 1: review ───────────────────── */
    .review-layout {
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 2rem;
      align-items: start;
    }
    @media (max-width: 800px) { .review-layout { grid-template-columns: 1fr; } }

    .items-block, .summary {
      padding: 2rem;
      background: linear-gradient(160deg, rgba(255,255,255,0.04), rgba(255,255,255,0.012));
      border: 1px solid var(--border-soft);
      border-radius: 18px;
    }

    .items { display: flex; flex-direction: column; gap: 1rem; }
    .item {
      display: grid;
      grid-template-columns: 60px 1fr auto;
      gap: 1rem;
      align-items: center;
      padding: 0.85rem;
      background: rgba(255,255,255,0.025);
      border: 1px solid var(--border-faint);
      border-radius: 12px;
    }
    .item img, .item .ph {
      width: 60px; height: 60px;
      border-radius: 8px;
      object-fit: cover;
      background: #1d2122;
    }
    .item-info { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
    .item-info strong { font-weight: 500; color: var(--text-primary); }
    .item-info .muted { font-size: 0.8rem; color: var(--text-tertiary); }
    .subtotal { font-family: var(--font-display); font-size: 1rem; font-weight: 500; color: var(--text-primary); }

    /* ─── Summary ──────────────────────────── */
    .lines { margin: 0 0 1.5rem; padding: 0; display: flex; flex-direction: column; gap: 0.6rem; }
    .lines > div { display: flex; justify-content: space-between; align-items: baseline; }
    .lines dt { color: var(--text-tertiary); font-size: 0.875rem; }
    .lines dd { margin: 0; color: var(--text-primary); font-weight: 500; }
    .lines .total-line {
      padding-top: 0.8rem;
      border-top: 1px solid var(--border-faint);
      margin-top: 0.4rem;
    }
    .lines .total-line dt { color: var(--text-primary); font-size: 0.95rem; }
    .lines .total-line dd {
      font-family: var(--font-display);
      font-size: 1.5rem;
      font-weight: 500;
      letter-spacing: -0.02em;
    }
    .grad {
      background: linear-gradient(135deg, #22d3ee, #8b5cf6);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .btn-premium.block { width: 100%; justify-content: center; padding: 1rem 1.5rem; }

    .back {
      display: block;
      text-align: center;
      margin-top: 1rem;
      color: var(--text-tertiary);
      text-decoration: none;
      font-size: 0.85rem;
      transition: color 0.3s ease;
    }
    .back:hover { color: var(--text-primary); }

    /* ─── Step 2: pay ──────────────────────── */
    .pay-layout {
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      gap: 2rem;
      align-items: start;
    }
    @media (max-width: 900px) { .pay-layout { grid-template-columns: 1fr; } }

    .card-block, .summary.side {
      padding: 2rem;
      background: linear-gradient(160deg, rgba(255,255,255,0.04), rgba(255,255,255,0.012));
      border: 1px solid var(--border-soft);
      border-radius: 18px;
    }

    /* ─── Card preview ─────────────────────── */
    .card-preview {
      position: relative;
      width: 100%;
      max-width: 400px;
      margin: 1rem auto 2rem;
      aspect-ratio: 1.586;
      perspective: 1200px;
    }
    .card-face {
      position: absolute;
      inset: 0;
      border-radius: 18px;
      padding: 1.5rem;
      backface-visibility: hidden;
      transform-style: preserve-3d;
      transition: transform 0.7s var(--ease-out-quart, ease);
      box-shadow: 0 30px 60px rgba(0,0,0,0.5);
      color: white;
      overflow: hidden;
    }
    .card-face.front {
      background:
        radial-gradient(circle at top right, rgba(255,255,255,0.12), transparent 50%),
        linear-gradient(135deg, #1d2122 0%, #0e1010 100%);
      border: 1px solid rgba(255,255,255,0.08);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-face.front::before {
      content: '';
      position: absolute;
      width: 180%;
      height: 180%;
      top: -40%; left: -40%;
      background: radial-gradient(circle, rgba(34,211,238,0.18) 0%, transparent 40%);
      filter: blur(40px);
      z-index: 0;
    }
    .card-face.front[data-brand="visa"]::before { background: radial-gradient(circle, rgba(26,90,255,0.25) 0%, transparent 40%); }
    .card-face.front[data-brand="mastercard"]::before { background: radial-gradient(circle, rgba(235,89,40,0.25) 0%, transparent 40%); }
    .card-face.front[data-brand="amex"]::before { background: radial-gradient(circle, rgba(0,99,167,0.25) 0%, transparent 40%); }
    .card-face.front > * { position: relative; z-index: 1; }

    .chip {
      width: 38px;
      height: 28px;
      border-radius: 5px;
      background: linear-gradient(135deg, #c8a44b, #b8943b);
      box-shadow: inset 0 -8px 12px rgba(0,0,0,0.2), inset 0 4px 8px rgba(255,255,255,0.2);
      position: relative;
    }
    .chip::before {
      content: '';
      position: absolute;
      inset: 4px;
      border: 1px solid rgba(0,0,0,0.2);
      border-radius: 3px;
    }

    .brand-mark {
      position: absolute;
      top: 1.5rem; right: 1.5rem;
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      color: rgba(255,255,255,0.85);
      text-transform: uppercase;
    }

    .card-number {
      font-family: 'Inter', monospace;
      font-size: 1.4rem;
      letter-spacing: 0.12em;
      font-weight: 500;
      color: rgba(255,255,255,0.95);
      margin: auto 0;
    }

    .card-row { display: flex; justify-content: space-between; gap: 1rem; }
    .card-row .lbl {
      display: block;
      font-size: 0.6rem;
      letter-spacing: 0.15em;
      color: rgba(255,255,255,0.55);
      margin-bottom: 0.2rem;
    }
    .card-row .val {
      font-family: 'Inter', monospace;
      font-size: 0.85rem;
      letter-spacing: 0.05em;
      color: rgba(255,255,255,0.9);
      text-transform: uppercase;
    }

    .card-face.back {
      background: linear-gradient(135deg, #1a1d1e 0%, #0a0c0c 100%);
      transform: rotateY(180deg);
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .card-preview.flipped .card-face.front { transform: rotateY(-180deg); }
    .card-preview.flipped .card-face.back { transform: rotateY(0); }

    .strip {
      width: calc(100% + 3rem);
      margin: 0 -1.5rem;
      height: 40px;
      background: #000;
      margin-top: 1.5rem;
    }
    .cvv-box {
      align-self: flex-end;
      background: rgba(255,255,255,0.85);
      color: #0b0c0c;
      padding: 0.6rem 1rem;
      border-radius: 5px;
      min-width: 80px;
      text-align: right;
    }
    .cvv-lbl { display: block; font-size: 0.55rem; letter-spacing: 0.15em; margin-bottom: 2px; }
    .cvv-val { font-family: 'Inter', monospace; font-size: 1rem; letter-spacing: 0.1em; }

    /* ─── Card form ───────────────────────── */
    .card-form { display: flex; flex-direction: column; gap: 1.25rem; }
    .form-row { display: flex; flex-direction: column; gap: 0.4rem; }
    .form-row label {
      font-size: 0.7rem;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--text-tertiary);
    }
    .form-row input {
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border-soft);
      border-radius: 10px;
      padding: 0.85rem 1rem;
      color: var(--text-primary);
      font-family: 'Inter', monospace;
      font-size: 0.95rem;
      letter-spacing: 0.04em;
      transition: border-color 0.3s ease, background 0.3s ease;
    }
    .form-row input:focus {
      outline: none;
      border-color: rgba(59,130,246,0.45);
      background: rgba(255,255,255,0.06);
    }
    .card-input-wrap { position: relative; }
    .card-input-wrap input { width: 100%; padding-right: 5rem; }
    .brand-icon {
      position: absolute;
      right: 1rem;
      top: 50%;
      transform: translateY(-50%);
      font-family: var(--font-display);
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      color: var(--text-tertiary);
      text-transform: uppercase;
    }
    .form-grid { display: grid; grid-template-columns: 1fr 1fr 1.4fr; gap: 0.75rem; }

    .alert-err {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.8rem 1rem;
      background: rgba(255,99,99,0.08);
      border: 1px solid rgba(255,99,99,0.3);
      border-radius: 10px;
      color: #ff8a8a;
      font-size: 0.85rem;
    }

    .security-row {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.75rem;
      color: var(--text-tertiary);
      margin-top: 0.5rem;
    }

    .back-btn {
      background: none;
      border: none;
      color: var(--text-tertiary);
      cursor: pointer;
      text-align: center;
      font-family: var(--font-body);
      font-size: 0.825rem;
      padding: 0.5rem;
      transition: color 0.3s ease;
    }
    .back-btn:hover:not(:disabled) { color: var(--text-primary); }

    /* ─── Mini-items sidebar ──────────────── */
    .items-mini {
      list-style: none;
      padding: 0;
      margin: 0 0 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
      max-height: 200px;
      overflow-y: auto;
    }
    .items-mini li {
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 0.6rem;
      align-items: center;
      font-size: 0.85rem;
      color: var(--text-secondary);
      padding-bottom: 0.4rem;
      border-bottom: 1px dashed var(--border-faint);
    }
    .items-mini .name { color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    /* ─── Result ──────────────────────────── */
    .result {
      max-width: 540px;
      margin: 2rem auto;
      padding: 3rem 2rem;
      text-align: center;
      background: linear-gradient(160deg, rgba(255,255,255,0.04), rgba(255,255,255,0.012));
      border: 1px solid var(--border-soft);
      border-radius: 24px;
    }
    .result h2 {
      font-family: var(--font-display);
      font-size: 2rem;
      font-weight: 500;
      letter-spacing: -0.025em;
      color: var(--text-primary);
      margin: 1rem 0 0.5rem;
    }
    .result .muted { color: var(--text-secondary); margin: 0; }

    .success-anim { display: grid; place-items: center; }
    .success-anim .ring { animation: drawRing 0.9s 0.1s var(--ease-out-quart) forwards; }
    .success-anim .check { animation: drawCheck 0.6s 0.7s var(--ease-out-quart) forwards; }
    @keyframes drawRing { to { stroke-dashoffset: 0; } }
    @keyframes drawCheck { to { stroke-dashoffset: 0; } }

    .receipt {
      margin: 2rem auto;
      padding: 1.25rem 1.5rem;
      background: rgba(255,255,255,0.025);
      border: 1px solid var(--border-faint);
      border-radius: 12px;
      max-width: 380px;
      text-align: left;
    }
    .r-row {
      display: flex;
      justify-content: space-between;
      padding: 0.45rem 0;
      border-bottom: 1px solid var(--border-faint);
      font-size: 0.85rem;
    }
    .r-row:last-child { border-bottom: none; }
    .r-row dt { color: var(--text-tertiary); }
    .r-row dd { margin: 0; color: var(--text-primary); font-family: 'Inter', monospace; }

    .success-actions {
      display: flex;
      gap: 0.75rem;
      justify-content: center;
      flex-wrap: wrap;
      margin-top: 1.5rem;
    }

    .fail-icon {
      filter: drop-shadow(0 0 30px rgba(255,99,99,0.3));
      margin-bottom: 1rem;
    }

    .empty-checkout {
      max-width: 480px;
      margin: 3rem auto;
      padding: 3rem 2rem;
      text-align: center;
      background: linear-gradient(160deg, rgba(255,255,255,0.04), rgba(255,255,255,0.012));
      border: 1px solid var(--border-soft);
      border-radius: 20px;
    }
    .empty-icon { font-size: 3rem; opacity: 0.6; margin-bottom: 1rem; }
    .empty-checkout h2 {
      font-family: var(--font-display);
      font-size: 1.5rem;
      font-weight: 500;
      margin: 0 0 0.5rem;
      color: var(--text-primary);
    }
    .empty-checkout p { color: var(--text-secondary); margin: 0 0 1.5rem; }

    .loading-wrap { padding: 4rem 0; display: grid; place-items: center; }

    .spin {
      display: inline-block;
      width: 14px; height: 14px;
      border: 1.5px solid rgba(0,0,0,0.2);
      border-top-color: currentColor;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  `]
})
export class CheckoutComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild('root') root!: ElementRef<HTMLElement>;
  @ViewChild('preview') previewEl?: ElementRef<HTMLElement>;

  cartSvc = inject(CartService);
  private payment = inject(PaymentService);
  private toast = inject(ToastService);
  auth = inject(AuthService);
  private router = inject(Router);
  private fb = inject(FormBuilder);
  private destroy$ = new Subject<void>();

  step = signal<Step>('review');
  loading = signal(true);
  cvvFocused = signal(false);
  paymentError = signal<string | null>(null);
  lastOrder = signal<Order | null>(null);
  lastTxnId = signal('');
  lastLast4 = signal('');

  form: FormGroup = this.fb.group({
    number: ['', [Validators.required]],
    name:   ['', [Validators.required, Validators.minLength(2)]],
    expiryMonth: ['', [Validators.required, Validators.pattern(/^\d{1,2}$/)]],
    expiryYear:  ['', [Validators.required, Validators.pattern(/^\d{2}$/)]],
    cvv:    ['', [Validators.required, Validators.pattern(/^\d{3,4}$/)]]
  });

  afterReview = computed(() => this.step() !== 'review');
  hasItems = computed(() => (this.cartSvc.cart()?.items?.length ?? 0) > 0);

  subtotal = computed(() => this.cartSvc.cart()?.total ?? 0);
  shipping = computed(() => this.subtotal() >= 500 ? 0 : 40);
  tax      = computed(() => Math.round(this.subtotal() * 0.2));
  total    = computed(() => Math.round(this.subtotal() + this.shipping() + this.tax()));

  brand = signal<CardBrand>('unknown');
  brandLabel = computed(() => {
    switch (this.brand()) {
      case 'visa': return 'VISA';
      case 'mastercard': return 'MASTERCARD';
      case 'amex': return 'AMEX';
      case 'discover': return 'DISCOVER';
      case 'maestro': return 'MAESTRO';
      default: return '';
    }
  });

  cardNumberMasked = computed(() => {
    const raw = (this.form.value.number || '').replace(/\D+/g, '');
    if (!raw) return '•••• •••• •••• ••••';
    const padded = raw.padEnd(16, '•');
    return padded.replace(/(.{4})/g, '$1 ').trim();
  });

  ngOnInit(): void {
    this.cartSvc.get()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => this.loading.set(false),
        error: () => this.loading.set(false)
      });

    // Track number changes to update brand
    this.form.get('number')!.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe((v: string) => {
        this.brand.set(this.payment.detectBrand(v));
      });
  }

  ngAfterViewInit(): void {
    gsap.fromTo(this.root.nativeElement,
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }
    );
  }

  goToPay(): void {
    if (!this.auth.isAuthenticated) {
      this.toast.error('Connectez-vous pour continuer');
      this.router.navigate(['/login']);
      return;
    }
    this.step.set('pay');
    this.paymentError.set(null);
  }

  onNumberInput(event: Event): void {
    const target = event.target as HTMLInputElement;
    const formatted = this.payment.formatNumber(target.value);
    this.form.patchValue({ number: formatted }, { emitEvent: true });
    // Reset cursor position handled by browser - acceptable for this UX
  }

  toUpper(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.form.patchValue({ name: target.value.toUpperCase() }, { emitEvent: false });
  }

  pay(): void {
    this.paymentError.set(null);

    const v = this.form.value;
    const card: CardData = {
      number: (v.number || '').replace(/\D+/g, ''),
      name: v.name,
      expiryMonth: v.expiryMonth.padStart(2, '0'),
      expiryYear: v.expiryYear,
      cvv: v.cvv
    };

    // Local pre-validate so we can show inline errors fast
    const valErr = this.payment.validate(card);
    if (valErr) {
      this.paymentError.set(valErr);
      return;
    }

    this.step.set('processing');

    this.payment.charge(card, this.total())
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (res) => {
          this.lastTxnId.set(res.transactionId);
          this.lastLast4.set(res.last4);
          this.lastOrder.set(res.order ?? null);
          this.step.set('success');
          this.cartSvc.get().subscribe();
          this.toast.success('Paiement confirmé · commande #' + (res.order?.id || '?'));
        },
        error: (err) => {
          this.paymentError.set(err?.reason || 'Erreur de traitement');
          this.step.set('failed');
        }
      });
  }

  retryPayment(): void {
    this.paymentError.set(null);
    this.step.set('pay');
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
