import {
  Component,
  ComponentFactoryResolver,
  ElementRef,
  Inject,
  Injector,
  OnInit,
  ViewChild,
} from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { finalize } from 'rxjs/operators';
import { ViewRecipeModel } from 'src/app/infrastructure/models/view-recipe.model';
import { AuthService } from 'src/app/infrastructure/services/auth.service';
import { FilesService } from 'src/app/infrastructure/services/files.service';
import { LoaderService } from 'src/app/infrastructure/services/loader.service';
import { RecipesService } from 'src/app/infrastructure/services/recipes.service';

@Component({
  selector: 'app-recipe',
  templateUrl: './recipe.component.html',
  styleUrls: ['./recipe.component.css'],
})
export class RecipeComponent implements OnInit {
  @ViewChild('recipeContainer', { static: false })
  recipeContainer: ElementRef;

  recipe: ViewRecipeModel;

  mainImageSrc: string = '#';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private loaderService: LoaderService,
    private recipesService: RecipesService,
    private filesService: FilesService,
    private sanitizer: DomSanitizer,
    private componentFactoryResolver: ComponentFactoryResolver,
    private injector: Injector,
    private authService: AuthService,
    @Inject('BASE_API_URL') private readonly baseApiUrl: string
  ) {}

  ngOnInit(): void {
    this.recipe = new ViewRecipeModel();

    this.route.paramMap.subscribe((params) => {
      const id = params.get('id');
      if (id) {
        this.fetchData(id);
      }
    });

    this.router.events.subscribe((evt) => {
      if (evt instanceof NavigationEnd) {
        window.scrollTo(0, 0);
      }
    });
  }

  private fetchData = (id: string): void => {
    this.loaderService.show();
    this.recipesService
      .getRecipeSinglePortal(id)
      .pipe(
        finalize(() => {
          this.loaderService.hide();
        })
      )
      .subscribe(
        (result) => {
          this.recipe = result;
          this.recipe.id = id;

          this.recipeContainer.nativeElement.innerHTML = result.content;

          this.setRecipeMainImg(+this.recipe.mainImageId);
        },
        (error) => {}
      );
  };

  private setRecipeMainImg = (id: number): void => {
    this.loaderService.show();
    this.filesService
      .getFileById(id)
      .pipe(
        finalize(() => {
          this.loaderService.hide();
        })
      )
      .subscribe(
        (result) => {
          this.setMainImgSrc(result.body);
        },
        (error) => {}
      );
  };

  private setMainImgSrc = (file: File | Blob): void => {
    let myReader: FileReader = new FileReader();
    let self = this;
    myReader.onloadend = function (e) {
      self.mainImageSrc = myReader.result.toString();
    };
    myReader.readAsDataURL(file);
  };
}
