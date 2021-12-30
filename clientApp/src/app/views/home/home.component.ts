import { Component, OnInit } from '@angular/core';
import { finalize } from 'rxjs/operators';
import { UserDetailsModel } from 'src/app/infrastructure/models/user-details.model';
import { LoaderService } from 'src/app/infrastructure/services/loader.service';
import { UserServiceService } from 'src/app/infrastructure/services/user-service.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  public usersList: UserDetailsModel[] = [];

  constructor(
    private loaderService: LoaderService,
    private userService: UserServiceService
  ) {}

  ngOnInit(): void {
    window.scrollTo(0, 0);
    this.fetchUsers();

    // TODO do usunięcia jak będą endpointy

    this.usersList = [
      {
        id: 1,
        username: 'Pawel123',
      },
      {
        id: 2,
        username: 'Sgewgerg',
      },
      {
        id: 3,
        username: 'Sgerger',
      },
      {
        id: 4,
        username: 'Hregreg',
      },
      {
        id: 5,
        username: 'Sger eg er ',
      },
    ];
  }

  private fetchUsers = (): void => {
    this.loaderService.show();
    this.userService
      .getAllUsers()
      .pipe(
        finalize(() => {
          this.loaderService.hide();
        })
      )
      .subscribe(
        (result) => {
          this.usersList = result;
        },
        (error) => {}
      );
  };
}
