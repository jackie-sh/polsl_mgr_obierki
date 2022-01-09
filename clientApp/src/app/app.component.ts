import { Component, OnInit } from '@angular/core';
import { ChatAdapter } from 'ng-chat';
import { AuthService } from './infrastructure/services/auth.service';
import { MyChatAdapter } from 'src/app/infrastructure/helpers/chat-adapter';
import { UserDetailsModel } from './infrastructure/models/user-details.model';
import { finalize } from 'rxjs/operators';
import { MessagesService } from './infrastructure/services/messages.service';
import { UserServiceService } from './infrastructure/services/user-service.service';
import { Location } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  title = 'clientApp';

  public adapter: MyChatAdapter = new MyChatAdapter();

  public chatTitle = 'Wyślij wiadomość';
  public messagePlaceholder = 'Napisz wiadomość';

  users: UserDetailsModel[] = [];

  constructor(
    private location: Location,
    private messagesService: MessagesService,
    private userService: UserServiceService,
    public authService: AuthService
  ) {}

  ngOnInit(): void {
    this.fetchData();
  }

  private fetchData = (): void => {
    this.userService
      .getAllUsers()
      .pipe(
        finalize(() => {
          let loggedId = this.authService.loggedId;

          for (var user of this.users) {
            if (user.id == +loggedId) {
              console.log('cont');
              continue;
            }
            this.adapter.addParticipand(user.id, user.username);
          }
        })
      )
      .subscribe(
        (result) => {
          this.users = result;
        },
        (error) => {}
      );
  };
}
