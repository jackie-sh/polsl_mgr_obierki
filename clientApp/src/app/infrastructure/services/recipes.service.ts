import { Injectable, Inject, EventEmitter } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs/internal/Observable';
import { Subject } from 'rxjs';
import { timeout } from 'rxjs/operators';
import { CreateRecipeModel } from 'src/app/infrastructure/models/createRecipe.model';
import { RecipeFileUploadModel } from 'src/app/infrastructure/models/RecipeFileUpload.model';
import { ViewRecipeModel } from '../models/view-recipe.model';

declare var tinyMCE: any;

@Injectable({
  providedIn: 'root',
})
export class RecipesService {
  messageSubject = new Subject();
  private invalidExtenstionName: string = '';

  constructor(
    @Inject('BASE_API_URL') private readonly baseApiUrl: string,
    private readonly http: HttpClient
  ) {}

  getRecipeForUpdate = (id: string): Observable<CreateRecipeModel> => {
    return this.http.get<CreateRecipeModel>(`${this.baseApiUrl}/recipe-edit/${id}`);
  };

  postRecipe = (model: CreateRecipeModel): Observable<Response> => {
    return this.http.post<Response>(`${this.baseApiUrl}/recipe-add`, model);
  };

  putRecipe = (model: CreateRecipeModel): Observable<Response> => {
    return this.http.put<Response>(`${this.baseApiUrl}/recipe-edit`, model);
  };

  postRecipeImage = (data: FormData): Observable<RecipeFileUploadModel> => {
    return this.http.post<RecipeFileUploadModel>(
      `${this.baseApiUrl}/recipe/recipe-image`,
      data
    );
  };

  getRecipeSinglePortal = (
    id: string
  ): Observable<ViewRecipeModel> => {
    return this.http.get<ViewRecipeModel>(
      `${this.baseApiUrl}/recipe/${id}`
    );
  };

  fileAddedEmitter = new Subject<string>();

  getRecipeTinyInit = (): any => {
    return {
      height: 500,
      plugins: 'code preview link image textpattern paste autolink',
      toolbar:
        'preview | undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | sizeselect | fontselect |  fontsizeselect',
      table_default_styles: {
        width: '100%',
        'max-width': '100%',
        'word-wrap': 'break-word',
        'table-layout': 'fixed',
      },
      table_responsive_width: true,
      menubar: 'tools insert',
      language: 'pl',
      a11y_advanced_options: true,
      automatic_uploads: true,
      image_title: true,
      relative_urls: false,
      remove_script_host: false,
      convert_urls: true,
      media_live_embeds: true,
      file_picker_types: 'image media',

      file_picker_callback: function (callback, value, meta) {
        var input = document.createElement('input');
        input.setAttribute('type', 'file');
        if (meta.filetype == 'image') {
          input.setAttribute('accept', 'image/*');
        }

        input.onchange = function () {
          var file = (<HTMLInputElement>this).files[0];

          var reader = new FileReader();
          reader.onload = function () {
            if (meta.filetype == 'image') {
              var id = 'blobid' + new Date().getTime();
              var blobCache = tinyMCE.activeEditor.editorUpload.blobCache;
              var base64 = (<string>reader.result).split(',')[1];
              var blobInfo = blobCache.create(id, file, base64);
              blobCache.add(blobInfo);
              callback(blobInfo.blobUri(), { title: file.name });
            }
          };
          reader.readAsDataURL(file);
        };

        input.dispatchEvent(new MouseEvent('click'));
      },
    };
  };

  invalidExtenstion() {
    this.messageSubject.next(this.invalidExtenstionName);
  }
}
