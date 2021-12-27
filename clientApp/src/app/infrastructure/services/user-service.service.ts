import { Injectable, Inject } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { UserDetailsModel } from "../models/user-details.model";
import { Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class UserServiceService {

  constructor(
    @Inject("BASE_API_URL") private readonly baseApiUrl: string,
    private readonly http: HttpClient
  ) {}

  getAllUsers = (): Observable<UserDetailsModel[]> => {
    return this.http.get<UserDetailsModel[]>(`${this.baseApiUrl}/users/getAllUsersr`, {});
  };
}
