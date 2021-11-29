import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UserSiteComponent } from './user-site.component';

describe('UserSiteComponent', () => {
  let component: UserSiteComponent;
  let fixture: ComponentFixture<UserSiteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UserSiteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserSiteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
