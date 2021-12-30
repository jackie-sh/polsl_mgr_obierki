import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CreateRecipeComponent } from './create-recipe/create-recipe.component';
import { RecipeComponent } from './recipe/recipe.component';

const routes: Routes = [
  {
    path: 'create-recipe',
    component: CreateRecipeComponent,
    data: {
      title: 'Dodaj przepis',
    },
  },
  {
    path: 'list-recipe',
    component: CreateRecipeComponent,
    data: {
      title: 'Lista przepisów',
    },
  },
  {
    path: 'create-recipe/:id',
    component: CreateRecipeComponent,
    data: {
      title: 'Edytuj przepis',
    },
  },
  {
    path: 'recipe-details/:id',
    component: RecipeComponent,
    data: {
      title: 'Przepis kulinarny',
    },
  },
  {
    path: '',
    redirectTo: 'create-recipe',
    pathMatch: 'full',
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class RecipeRoutingModule {}
