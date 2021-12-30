import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { FooterComponent } from './shared/footer/footer.component';
import { HomeComponent } from './views/home/home.component';
import { LoaderComponent } from './shared/loader/loader.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AboutComponent } from './views/about/about.component';
import { CreateRecipeComponent } from './views/recipes/create-recipe/create-recipe.component';
import { ConfirmationComponent } from './shared/confirmation/confirmation.component';
import { EditorModule } from '@tinymce/tinymce-angular';
import { NgbModule, NgbRatingModule } from '@ng-bootstrap/ng-bootstrap';
import { RecipesListComponent } from './views/recipes/recipes-list/recipes-list.component';
import { MyProfileComponent } from './views/user/my-profile/my-profile.component';
import { RecipesFilterComponent } from './views/recipes/recipes-filter/recipes-filter.component';
import { AppHelper } from 'src/app/infrastructure/helpers/app-helper';
import { JwtModule } from '@auth0/angular-jwt';
import { NgChatModule } from 'ng-chat';
import { RecipeComponent } from './views/recipes/recipe/recipe.component';
import { UserProfileComponent } from './views/user/user-profile/user-profile.component';

export function tokenGetter() {
  return localStorage.getItem('ACCESS_TOKEN');
}

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    HomeComponent,
    LoaderComponent,
    AboutComponent,
    CreateRecipeComponent,
    RecipesListComponent,
    ConfirmationComponent,
    MyProfileComponent,
    RecipesFilterComponent,
    RecipeComponent,
    UserProfileComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NoopAnimationsModule,
    ReactiveFormsModule,
    FormsModule,
    EditorModule,
    NgbModule,
    NgbRatingModule,
    NgChatModule,
    JwtModule.forRoot({
      config: {
        tokenGetter: tokenGetter,
        allowedDomains: [AppHelper.getBaseUrl()],
        disallowedRoutes: [],
      },
    }),
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
