import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { SendMessageModel } from 'src/app/infrastructure/models/send-message.model';

@Injectable({
  providedIn: 'root',
})
export class MessagesService {
  constructor(
    @Inject('BASE_API_URL') private readonly baseApiUrl: string,
    private readonly http: HttpClient
  ) {}

  getMessages = (
    fromUserId: string,
    toUserId: string
  ): Observable<SendMessageModel[]> => {
    return this.http.get<SendMessageModel[]>(
      `${this.baseApiUrl}/messages/getMessages?fromUserId=${fromUserId}&toUserId=${toUserId}`
    );
  };

  sendMessage = (model: SendMessageModel): Observable<Response> => {
    return this.http.post<Response>(
      `${this.baseApiUrl}/messages/sendMesssage`,
      model
    );
  };
}
