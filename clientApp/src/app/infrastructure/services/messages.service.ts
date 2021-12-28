import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class MessagesService {
  constructor(
    @Inject('BASE_API_URL') private readonly baseApiUrl: string,
    private readonly http: HttpClient
  ) {}
}
