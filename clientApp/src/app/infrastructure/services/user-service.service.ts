import { Injectable, Inject } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { UserRegisterModel } from "../models/userRegister.model";

@Injectable({
  providedIn: 'root'
})
export class UserServiceService {

  constructor(
    @Inject("BASE_API_URL") private readonly baseApiUrl: string,
    private readonly http: HttpClient
  ) {}

  userRegister = (model: UserRegisterModel) => {
    const url = `${this.baseApiUrl}/register`;
    return this.http.post<any>(url, model);
  };
}
