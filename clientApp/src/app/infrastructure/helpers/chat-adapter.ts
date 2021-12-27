import {
  ChatAdapter,
  IChatGroupAdapter,
  User,
  Group,
  Message,
  ChatParticipantStatus,
  ParticipantResponse,
  ParticipantMetadata,
  ChatParticipantType,
  IChatParticipant,
} from 'ng-chat';
import { Observable, of } from 'rxjs';
import { delay, finalize } from 'rxjs/operators';
import { UserDetailsModel } from '../models/user-details.model';
import { UserServiceService } from '../services/user-service.service';
import { MessagesService } from '../services/messages.service';
import { Component, OnInit } from '@angular/core';

export class MyChatAdapter extends ChatAdapter {
  public mockedParticipants: IChatParticipant[] = [];

  addParticipand(id: number, name: string) {
    this.mockedParticipants.push({
      participantType: ChatParticipantType.User,
      id: id,
      displayName: name,
      avatar:
        'https://img.myloview.pl/tapety/hand-drawn-modern-man-avatar-profile-icon-or-portrait-icon-user-flat-avatar-icon-sign-profile-male-symbol-700-234216721.jpg',
      status: ChatParticipantStatus.Offline,
    });
  }

  listFriends(): Observable<ParticipantResponse[]> {
    return of(
      this.mockedParticipants.map((user) => {
        let participantResponse = new ParticipantResponse();

        participantResponse.participant = user;

        return participantResponse;
      })
    );
  }

  public onFriendsListChanged(
    participantsResponse: ParticipantResponse[]
  ): void {}

  getMessageHistory(destinataryId: any): Observable<Message[]> {
    let mockedHistory: Array<Message> = [];

    /*
    mockedHistory = [
      {
        fromId: 1,
        toId: 999,
        message:
          'Message',
        dateSent: new Date(),
      },
    ];
    */
    return of(mockedHistory).pipe(delay(0));
  }

  sendMessage(message: Message): void {}
}
