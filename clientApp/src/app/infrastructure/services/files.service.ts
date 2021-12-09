import { Injectable, Inject } from "@angular/core";
import { HttpClient, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs/internal/Observable";

@Injectable({
  providedIn: 'root'
})
export class FilesService {

  constructor(
    @Inject("BASE_API_URL") private readonly baseApiUrl: string,
    private readonly http: HttpClient
  ) {}

  getFileById = (
    id: string,
  ): Observable<HttpResponse<Blob>> => {
    return this.http.get(
      `${this.baseApiUrl}/files/${id}/`,
      {
        responseType: "blob",
        observe: "response",
      }
    );
  };
}