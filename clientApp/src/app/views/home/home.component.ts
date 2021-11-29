import { Component, OnInit } from '@angular/core';
import { LoaderService } from 'src/app/infrastructure/services/loader.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private loaderService: LoaderService) { }

  ngOnInit(): void {
  //  this.loaderService.show();
  }
}
