import { NgModule } from '@angular/core';
import { Routes, RouterModule, Route } from '@angular/router';
import { AboutComponent } from './views/about/about.component';
import { HomeComponent } from './views/home/home.component';
import { MyProfileComponent } from './views/user/my-profile/my-profile.component';
import { UserSiteComponent } from './views/user/user-site/user-site.component';

const routes: Route[] = [
  {
    path: 'home',
    component: HomeComponent,
    data: {
      title: 'Strona główna',
      breadcrumbs: 'Strona główna',
    },
  },
  {
    path: 'about',
    component: AboutComponent,
    data: {
      title: 'O nas',
      breadcrumbs: 'O nas',
    },
  },
  {
    path: 'user/:id',
    component: UserSiteComponent,
    data: {
      title: 'Użytkownik',
      breadcrumbs: 'Użytkownik',
    },
  },
  {
    path: 'my-profile',
    component: MyProfileComponent,
    data: {
      title: 'Mój profil',
      breadcrumbs: 'Mój profil',
    },
  },
  {
    path: 'auth',
    loadChildren: () =>
      import('./views/auth/auth.module').then((m) => m.AuthModule),
    data: {
      title: 'Logowanie i rejestracja',
      breadcrumbs: null,
    },
  },
  {
    path: 'recipe',
    loadChildren: () =>
      import('./views/recipes/recipe.module').then((m) => m.RecipeModule),
    data: {
      title: 'Przepisy',
      breadcrumbs: null,
    },
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
