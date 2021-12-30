import { NgModule } from '@angular/core';
import { Routes, RouterModule, Route } from '@angular/router';
import { AboutComponent } from './views/about/about.component';
import { HomeComponent } from './views/home/home.component';
import { CreateRecipeComponent } from './views/recipes/create-recipe/create-recipe.component';
import { RecipeComponent } from './views/recipes/recipe/recipe.component';
import { MyProfileComponent } from './views/user/my-profile/my-profile.component';

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
    path: 'recipe/details/:id',
    component: RecipeComponent,
    data: {
      title: 'Przepis kulinarny',
    },
  },
  {
    path: 'recipe/create-recipe',
    component: CreateRecipeComponent,
    data: {
      title: 'Edytuj przepis',
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
