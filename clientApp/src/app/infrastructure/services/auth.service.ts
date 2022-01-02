import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRouteSnapshot, Router } from '@angular/router';
import { LoaderService } from './loader.service';
import { RegisterModel } from '../models/register.model';
import { tap, share, finalize, take, map } from 'rxjs/operators';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Moment } from 'moment';
import * as moment from 'moment';

const USER_ID_NAME: string = 'USER_ID';
const USERNAME_EMAIL: string = 'EMAIL';
const USERNAME_LOGIN: string = 'LOGIN';
const ACCESS_TOKEN_NAME: string = 'ACCESS_TOKEN';
const REFRESH_TOKEN_NAME: string = 'REFRESH_TOKEN';
const EXPIRATION_DATE_NAME: string = 'EXPIRATION_DATE';
const REFRESH_TOKEN_INTERVAL_MILIS: string = 'REFRESH_TOKEN_INTERVAL';

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

  private refreshService: Subscription = null;
  public tokenSubscriber: Subject<string>;

  constructor(
    @Inject('BASE_API_URL') private readonly baseApiUrl: string,
    private readonly http: HttpClient,
    private router: Router,
    private loaderService: LoaderService
  ) {
    this.tokenSubscriber = new Subject<string>();
    this.refreshToken((response) => {
      this.createRefreshService(+localStorage.getItem(EXPIRATION_DATE_NAME));
    });
  }

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
    return this.http.post<any>(`${this.baseApiUrl}/login`, model).pipe(
      tap(async (res) => {
        this.setLocalStorage(await res);

        this.loggedInSubject.next(true);
        this.tokenSubscriber.next(res.token);
      }),
      finalize(() => {})
    );
  };

  private setLocalStorage = (response: any): void => {
    const helper = new JwtHelperService();

    const decodetdTokenAccess = helper.decodeToken(response.accessToken);
    const decodetdTokenRefresh = helper.decodeToken(response.refreshToken);

    localStorage.setItem(USER_ID_NAME, response.id);

    console.log(decodetdTokenAccess);
    console.log(decodetdTokenRefresh);

    localStorage.setItem(ACCESS_TOKEN_NAME, response.accessToken); // access token
    localStorage.setItem(REFRESH_TOKEN_NAME, response.refreshToken); // refresh token

    //  localStorage.setItem(USERNAME_LOGIN, decodetdTokenAccess.username);

    localStorage.setItem(EXPIRATION_DATE_NAME, decodetdTokenAccess.exp); // token exporation date
    localStorage.setItem(
      REFRESH_TOKEN_INTERVAL_MILIS,
      decodetdTokenRefresh.exp
    ); // token exporation dat

    this.createRefreshService(decodetdTokenAccess.exp);
  };

  public logOut = async (): Promise<void> => {
    this.loaderService.show();
    if (this.isLoggedIn) {
      this.http
        .post<void>(`${this.baseApiUrl}/auth/logout`, {})
        .pipe(
          finalize(() => {
            this.clearLocalStorage();
            this.destroyRefreshService();
            this.loggedInSubject.next(false);
            this.tokenSubscriber.next(null);
            this.loaderService.hide();
            this.router.navigate(['/home'], {
              queryParams: { logoutSuccess: 'true' },
            });
          })
        )
        .subscribe(
          (result) => {},
          (error) => {}
        );
    } else {
      this.loaderService.hide();
    }
  };

  private clearLocalStorage = (): void => {
    console.log('clear token values');

    localStorage.removeItem(USERNAME_LOGIN);
    localStorage.removeItem(USER_ID_NAME);
    localStorage.removeItem(REFRESH_TOKEN_NAME);
    localStorage.removeItem(ACCESS_TOKEN_NAME);
    localStorage.removeItem(EXPIRATION_DATE_NAME);
    localStorage.removeItem(REFRESH_TOKEN_INTERVAL_MILIS);
  };

  private destroyRefreshService = (): void => {
    if (this.refreshService) this.refreshService.unsubscribe();
    this.refreshService = null;
  };

  private createRefreshService = (expirationMs: number): void => {
    this.destroyRefreshService();
    const intervalInMiliseconds = expirationMs;

    if (this.refreshService) return;

    console.log('Interval:');
    console.log(intervalInMiliseconds);

    this.refreshService = interval(intervalInMiliseconds).subscribe(() =>
      this.refreshToken()
    );
  };

  public refreshToken = (pipe: (response) => void = (response) => {}) => {
    console.log('refreshing token');
    const token = localStorage.getItem(ACCESS_TOKEN_NAME);
    const refreshToken = localStorage.getItem(REFRESH_TOKEN_NAME);
    if (token && refreshToken) {
      const params = { accessToken: token, refreshToken: refreshToken };
      this.http
        .post<any>(`${this.baseApiUrl}/refresh-token`, params)
        .pipe(
          finalize(() => {
            this.removeOldToken(token, refreshToken);
          })
        )
        .subscribe(
          (res: any) => {
            this.updateTokenValues(res);
            pipe(res);
            this.tokenSubscriber.next(res.token);
          }
          //  () => this.logOut()
        );
    }
  };

  private removeOldToken = (token: string, refreshToken: string): void => {
    // TODO ???
    /*
    if (token && refreshToken) {
      const params = { accessToken: token, refreshToken: refreshToken };
      this.http.post<any>(`${this.baseApiUrl}/auth/DeleteJwtToken`, params);
    }
    */
  };

  private updateTokenValues = (response: any): void => {
    console.log('update token values');

    const helper = new JwtHelperService();

    const decodetdTokenAccess = helper.decodeToken(response.accessToken);
    const decodetdTokenRefresh = helper.decodeToken(response.refreshToken);

    localStorage.setItem(ACCESS_TOKEN_NAME, response.accessToken); // access token
    localStorage.setItem(REFRESH_TOKEN_NAME, response.refreshToken); // refresh token

    localStorage.setItem(EXPIRATION_DATE_NAME, decodetdTokenAccess.exp); // token exporation date
    localStorage.setItem(
      REFRESH_TOKEN_INTERVAL_MILIS,
      decodetdTokenRefresh.exp
    ); // token exporation date
  };
}
