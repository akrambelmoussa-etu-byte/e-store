import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { ToastService } from '../services/toast.service';

export const adminGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const toast = inject(ToastService);

  if (auth.isAuthenticated && auth.isAdmin) {
    return true;
  }

  if (!auth.isAuthenticated) {
    toast.error('Connexion requise');
    router.navigate(['/login']);
    return false;
  }

  toast.error('Accès réservé à l\'administration');
  router.navigate(['/']);
  return false;
};
