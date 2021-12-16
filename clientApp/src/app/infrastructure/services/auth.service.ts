import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRouteSnapshot, Router } from '@angular/router';
import { LoaderService } from './loader.service';
import { RegisterModel } from '../models/register.model';
import { tap, share, finalize, take, map } from 'rxjs/operators';
import { JwtHelperService } from '@auth0/angular-jwt';

const USER_ID_NAME: string = 'USER_ID';
const USERNAME_EMAIL: string = 'EMAIL';
const USERNAME_LOGIN: string = 'LOGIN';
const ACCESS_TOKEN_NAME: string = 'ACCESS_TOKEN';

import {
  Observable,
  interval,
  Subscription,
  of,
  Subscriber,
  Subject,
  BehaviorSubject,
} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  loggedInSubject: Subject<boolean> = new Subject<boolean>();

  constructor(
    @Inject('BASE_API_URL') private readonly baseApiUrl: string,
    private readonly http: HttpClient,
    private router: Router,
    private loaderService: LoaderService
  ) {}

  get loggedUserName() {
    return localStorage.getItem(USERNAME_LOGIN);
  }

  get loggedId() {
    return localStorage.getItem(USER_ID_NAME);
  }

  get isLoggedIn(): boolean {
    return !!localStorage.getItem(ACCESS_TOKEN_NAME);
  }

  register = (model: RegisterModel): Observable<any> => {
    return this.http.post<any>(`${this.baseApiUrl}/register`, model);
  };

  login = (model: { username: string; password: string }): Observable<any> => {
    console.log(model);
    return this.http.post<any>(`${this.baseApiUrl}/login`, model).pipe(
      tap(async (res) => {
        console.log(res);
        this.setLocalStorage(await res);
        this.loggedInSubject.next(true);
      }),
      finalize(() => {})
    );
  };

  private setLocalStorage = (response: any): void => {
    const helper = new JwtHelperService();

    const decodedToken = helper.decodeToken(response.token);

    console.log(decodedToken);

    localStorage.setItem(ACCESS_TOKEN_NAME, response.token);
    //localStorage.setItem(USER_ID_NAME, response.user_id);
    //localStorage.setItem(USERNAME_EMAIL, response.email);
    localStorage.setItem(USERNAME_LOGIN, decodedToken.username);
  };

  public logOut = async (): Promise<void> => {
    this.loaderService.show();
    if (this.isLoggedIn) {
      this.http
        .post<void>(`${this.baseApiUrl}/auth/logout`, {})
        .pipe(
          finalize(() => {
            this.clearLocalStorage();
            this.loaderService.hide();

            this.router.navigate(['/home'], {
              queryParams: { logoutSuccess: 'true' },
            });
          })
        )
        .subscribe(
          (result) => {
            this.loggedInSubject.next(false);
          },
          (error) => {}
        );
    } else {
      this.loaderService.hide();
    }
  };

  private clearLocalStorage = (): void => {
    //localStorage.removeItem(USERNAME_EMAIL);
    localStorage.removeItem(USERNAME_LOGIN);
    localStorage.removeItem(ACCESS_TOKEN_NAME);
    //localStorage.removeItem(USER_ID_NAME);
  };
}
