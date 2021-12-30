import { NgModule } from '@angular/core';
import { EditorModule } from '@tinymce/tinymce-angular';
import { RecipeRoutingModule } from './recipe-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RecipeComponent } from './recipe/recipe.component';
import { NgbRatingModule } from '@ng-bootstrap/ng-bootstrap';
import { CommonModule } from '@angular/common';

@NgModule({
  declarations: [RecipeComponent],
  imports: [
    RecipeRoutingModule,
    EditorModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    NgbRatingModule,
  ],
})
export class RecipeModule {}
