import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EditorModule } from '@tinymce/tinymce-angular';
import { RecipeRoutingModule } from './recipe-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RecipeComponent } from './recipe/recipe.component';
import { NgbRatingModule } from '@ng-bootstrap/ng-bootstrap';
import { RecipesListComponent } from './recipes-list/recipes-list.component';
import { RecipesFilterComponent } from './recipes-filter/recipes-filter.component';

@NgModule({
  declarations: [RecipeComponent],
  imports: [
    CommonModule,
    RecipeRoutingModule,
    EditorModule,
    FormsModule,
    ReactiveFormsModule,
    NgbRatingModule,
  ],
})
export class RecipeModule {}
