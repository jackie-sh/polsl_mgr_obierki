import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {CreateRecipeComponent} from './create-recipe/create-recipe.component';

const routes: Routes = [
  {
    path: "create-recipe",
    component: CreateRecipeComponent,
    data: {
      title: "Dodaj przepis",
    },
  },
  {
    path: "create-recipe/:id",
    component: CreateRecipeComponent,
    data: {
      title: "Edytuj przepis",
    },
  },
  {
    path: "",
    redirectTo: "create-recipe",
    pathMatch: "full",
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RecipeRoutingModule { }
