export type Role = 'USER' | 'ADMIN';

export interface User {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  role: Role;
}

export interface Profile {
  phone?: string;
  address?: string;
  city?: string;
  country?: string;
}

export interface UserDetails {
  user: User;
  profile: Profile;
}

export interface AuthResponse {
  token: string;
  user: User;
}
