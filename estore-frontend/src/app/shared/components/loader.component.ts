import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-loader',
  standalone: true,
  template: `
    <div class="d-flex justify-content-center align-items-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
      @if (message) {
        <span class="ms-3 text-muted">{{ message }}</span>
      }
    </div>
  `
})
export class LoaderComponent {
  @Input() message = '';
}
