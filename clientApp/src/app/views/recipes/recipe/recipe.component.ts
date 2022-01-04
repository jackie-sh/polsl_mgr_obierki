import {
  Component,
  ComponentFactoryResolver,
  ElementRef,
  Inject,
  Injector,
  OnInit,
  ViewChild,
} from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { finalize } from 'rxjs/operators';
import { CategoryModel } from 'src/app/infrastructure/models/category.model';
import { CommentModel } from 'src/app/infrastructure/models/comment.model';
import { CreateCommentModel } from 'src/app/infrastructure/models/create-comment.model';
import { GetRecipeModel } from 'src/app/infrastructure/models/get-recipe.model';
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

  recipe: GetRecipeModel = new GetRecipeModel();

  comment: CreateCommentModel = new CreateCommentModel();

  mainImageSrc: string = '#';

  commentForm: FormGroup;

  isCommentFormInvalid: boolean;

  public categories: CategoryModel[] = [];

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
    window.scrollTo(0, 0);
    this.recipe = new GetRecipeModel();

    //TODO do wywalenia jak będą endpointy
    this.recipe.title = 'Testowy tytuł artykułu';
    this.recipe.content =
      ' <h1>Headings</h1><h2>are</h2><h3>great</h3><h4>for</h4><h5>titles</h5><h6>and subtitles</h6>';
    this.recipe.authorName = 'Pawel123';
    this.recipe.mainImageId = 2;
    this.recipe.recipeId = 3;
    this.recipe.authorId = 3;
    this.recipe.createdDate = new Date();
    this.recipe.categoryId = 2;
    this.recipe.rating = 4.6;
    this.recipe.shortDescription = 'Jakiś krótki opis artykułu o czym on jest';
    this.recipe.views = 100;
    this.recipe.comments = [
      {
        userId: '10',
        content: 'Fajny przepis :))))))))))))))))))))))',
        rating: 5,
        userName: 'Pawel132',
      },
      {
        userId: '20',
        content: 'Nie podoba mi sie',
        rating: 2,
        userName: 'Aasfksofj',
      },
    ];

    this.route.paramMap.subscribe((params) => {
      const id = params.get('id');
      if (id) {
        this.fetchData(id);
        this.initForm();
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
      .getRecipeDetails(id)
      .pipe(
        finalize(() => {
          this.loaderService.hide();

          //TODO do wywalenia
          this.recipeContainer.nativeElement.innerHTML = this.recipe.content;
        })
      )
      .subscribe(
        (result) => {
          this.recipe = result;

          this.recipeContainer.nativeElement.innerHTML = result.content;

          this.setRecipeMainImg(+this.recipe.mainImageId);
        },
        (error) => {}
      );

    this.loaderService.show();

    this.recipesService
      .getRecipeCategories()
      .pipe(
        finalize(() => {
          this.loaderService.hide();
        })
      )
      .subscribe(
        (result) => {
          if (result) {
            this.categories = result;
          }
        },
        (error) => {}
      );
  };

  public getCategoryName(id: number): string {
    if (id > this.categories.length || id == 0) {
      return 'brak kategorii';
    }

    return this.categories.filter(function (item) {
      return item.id === id;
    })[0].name;
  }

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

  private initForm = (): void => {
    let controls = {};

    controls['comment'] = new FormControl('', Validators.required);

    controls['rating'] = new FormControl(5, Validators.required);

    this.commentForm = new FormGroup(controls);
  };

  public sendComment() {
    this.validateForm();
    if (!this.isCommentFormInvalid) {
      this.loaderService.show();
      this.updateCommentModel();
      this.recipesService
        .createCommentForRecipe(this.comment)
        .pipe(
          finalize(() => {
            this.loaderService.hide();
          })
        )
        .subscribe(
          (result) => {
            window.location.reload();
          },
          (error) => {}
        );
    }
  }

  private validateForm = (): void => {
    this.commentForm.markAllAsTouched();
    this.isCommentFormInvalid = this.commentForm.invalid;
  };

  private updateCommentModel = (): void => {
    this.comment.commentText = this.commentContentControl.value;
    this.comment.rating = this.commentRatingControl.value;
    this.comment.recipeId = this.recipe.recipeId;
    this.comment.authorId = this.authService.loggedId;
  };

  get commentContentControl() {
    return this.commentForm.get('comment');
  }

  get commentRatingControl() {
    return this.commentForm.get('rating');
  }

  get isCommentinvalid() {
    return (
      this.commentContentControl.invalid &&
      this.commentContentControl.touched &&
      this.commentContentControl.errors &&
      this.commentContentControl.errors.required
    );
  }
}
