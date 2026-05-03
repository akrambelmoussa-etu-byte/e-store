import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { ToastService } from '../services/toast.service';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const toast = inject(ToastService);
  const auth = inject(AuthService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((err: HttpErrorResponse) => {
      const msg = err.error?.message || `Erreur HTTP ${err.status}`;
      if (err.status === 401) {
        auth.logout();
        router.navigate(['/login']);
        toast.error('Session expirée, veuillez vous reconnecter');
      } else if (err.status !== 0) {
        toast.error(msg);
      } else {
        toast.error('Serveur injoignable');
      }
      return throwError(() => err);
    })
  );
};
