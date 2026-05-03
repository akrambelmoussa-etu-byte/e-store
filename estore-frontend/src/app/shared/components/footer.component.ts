import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  standalone: true,
  template: `
    <footer class="bg-light border-top mt-5 py-4">
      <div class="container text-center text-muted small">
        © {{ year }} E-Store — Mini-projet Full-Stack — Akram Belmoussa &amp; Nouhaila Ben Soumane
        <br />
        Pr. Omar Zahour — Faculté des Sciences Ben M'Sick — Université Hassan II
      </div>
    </footer>
  `
})
export class FooterComponent {
  year = new Date().getFullYear();
}
