import { Injectable, Inject } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { ActivatedRouteSnapshot, Router } from "@angular/router";
import { LoaderService } from "./loader.service";
import { RegisterModel } from "../models/register.model";
import { tap, share, finalize, take, map } from "rxjs/operators";

const USER_ID_NAME: string = "USER_ID";
const USERNAME_NAME: string = "USERNAME";
const ACCESS_TOKEN_NAME: string = "ACCESS_TOKEN";

import {
  Observable,
  interval,
  Subscription,
  of,
  Subscriber,
  Subject,
  empty,
  BehaviorSubject,
} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  loggedInSubject: Subject<boolean> = new Subject<boolean>();

  constructor(
    @Inject("BASE_API_URL") private readonly baseApiUrl: string,
    private readonly http: HttpClient,
    private router: Router,
    private loaderService: LoaderService
  ) {

  }

  get loggedUserName() {
    return localStorage.getItem(USERNAME_NAME);
  }

  get loggedId() {
    return localStorage.getItem(USER_ID_NAME);
  }

  get isLoggedIn(): boolean {
    return !!localStorage.getItem(ACCESS_TOKEN_NAME);
  }

  register = (model: RegisterModel): Observable<Response> => {
    return this.http.post<Response>(`${this.baseApiUrl}`, model);
  };

  login = (model: { login: string; password: string }): Observable<any> => {
    return this.http.post<any>(`${this.baseApiUrl}/login`, model).pipe(
      tap(async (res) => {
        this.setLocalStorage(await res);
        this.loggedInSubject.next(true);
      }),
      finalize(() => {

      })
    );
  };

  private setLocalStorage = (response: any): void => {
    // TODO
  };

  public logOut = async (): Promise<void> => {
    this.loaderService.show();
    if (this.isLoggedIn) {
      this.http
        .post<void>(`${this.baseApiUrl}/auth/logout`, {})
        .pipe(
          finalize(() => {
            this.loaderService.hide();

            this.router.navigate(["/home"], {
              queryParams: { logoutSuccess: "true" },
            });
          })
        )
        .subscribe(
          (result) => {
            this.clearLocalStorage();
            this.loggedInSubject.next(false);
          },
          (error) => {}
        );
    } else {
      this.loaderService.hide();
    }
  };

  private clearLocalStorage = (): void => {
    localStorage.removeItem(USERNAME_NAME);
    localStorage.removeItem(ACCESS_TOKEN_NAME);
    localStorage.removeItem(USER_ID_NAME);
  };
}

