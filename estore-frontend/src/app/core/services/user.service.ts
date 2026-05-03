import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ApiResponse } from '../models/api-response.model';
import { Profile, UserDetails } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/users`;

  me(): Observable<ApiResponse<UserDetails>> {
    return this.http.get<ApiResponse<UserDetails>>(`${this.base}/me`);
  }

  updateMe(payload: { firstName?: string; lastName?: string; profile?: Profile }): Observable<
    ApiResponse<UserDetails>
  > {
    return this.http.put<ApiResponse<UserDetails>>(`${this.base}/me`, payload);
  }
}
