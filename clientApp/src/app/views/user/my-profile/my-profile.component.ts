import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FilesService } from 'src/app/infrastructure/services/files.service';
import { LoaderService } from 'src/app/infrastructure/services/loader.service';
import { RecipesService } from 'src/app/infrastructure/services/recipes.service';
import { UserServiceService } from 'src/app/infrastructure/services/user-service.service';
import { Location } from '@angular/common';
import { GetUserRecipeListItemModel } from 'src/app/infrastructure/models/get-user-recipe-list-item.model';
import { UserInfoModel } from 'src/app/infrastructure/models/user-info.model';
import { AuthService } from 'src/app/infrastructure/services/auth.service';
import { finalize } from 'rxjs/operators';
import { CategoryModel } from 'src/app/infrastructure/models/category.model';
import { ConfirmationService } from 'src/app/infrastructure/services/confirmation.service';

@Component({
  selector: 'app-my-profile',
  templateUrl: './my-profile.component.html',
  styleUrls: ['./my-profile.component.css'],
})
export class MyProfileComponent implements OnInit {
  public userRecipes: GetUserRecipeListItemModel[] = [];
  public userInfo: UserInfoModel = new UserInfoModel();

  public categories: CategoryModel[] = [
    { id: 1, name: 'Śniadanie' },
    { id: 2, name: 'Obiad' },
    { id: 3, name: 'Deser' },
    { id: 4, name: 'Podwieczorek' },
    { id: 5, name: 'Kolacja' },
  ];

  constructor(
    private location: Location,
    private route: ActivatedRoute,
    private router: Router,
    private loaderService: LoaderService,
    private recipesService: RecipesService,
    private filesService: FilesService,
    private userService: UserServiceService,
    private authService: AuthService,
    private confirmationService: ConfirmationService
  ) {}

  ngOnInit(): void {
    this.fetchData();

    // TODO do usunięcia jak będą endpointy
    this.userRecipes = [
      {
        title: 'przepis 1',
        authorName: 'Pawelek13',
        recipeId: '35',
        authorId: '43',
        shortDescription: 'jakiś tam krótki opis o przepisie',
        mainImageId: 10,
        rating: 3,
        categoryId: 2,
        createdDate: new Date(),
        mainImageSrc:
          'https://image.ceneostatic.pl/data/products/112187433/i-meal-box-tajski-kurczak-z-ryzem-i-warzywami-360g.jpg',
      },
      {
        title: 'przepis 2',
        authorName: 'Pawelek13',
        recipeId: '45',
        authorId: '45',
        shortDescription: 'jakiś tam krótki opis o przepisie 2',
        mainImageId: 10,
        rating: 3,
        categoryId: 2,
        createdDate: new Date(),
        mainImageSrc:
          'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.heb.com%2Fproduct-detail%2Fh-e-b-meal-simple-chicken-breast-southwest-marinade-potatoes-green-beans%2F2718585&psig=AOvVaw0EIYo_-5EM-5ZXdk2v12RC&ust=1640959106439000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCJDv_5fXi_UCFQAAAAAdAAAAABAJ',
      },
    ];

    this.userInfo.name = 'Pawelek13';
    this.userInfo.rating = 4.23;
    this.userInfo.views = 100;
    this.userInfo.userId = '2';
  }

  private fetchData = (): void => {
    this.loaderService.show();
    this.userService
      .getUserProfile(this.authService.loggedId)
      .pipe(
        finalize(() => {
          this.loaderService.hide();
        })
      )
      .subscribe(
        (result) => {
          this.userInfo = result;
        },
        (error) => {}
      );

    this.loaderService.show();
    this.userService
      .getUserRecipes(this.authService.loggedId)
      .pipe(
        finalize(() => {
          this.setRecipeMainImg();
          this.loaderService.hide();
        })
      )
      .subscribe(
        (result) => {
          this.userRecipes = result;
        },
        (error) => {}
      );
  };

  private setRecipeMainImg = (): void => {
    this.userRecipes.forEach((x) => {
      if (x.mainImageId != null) {
        this.filesService
          .getFileById(x.mainImageId)
          .pipe(finalize(() => {}))
          .subscribe(
            (result) => {
              this.setMainImgSrc(x, result.body);
            },
            (error) => {}
          );
      }
    });
  };

  public getCategoryName(id: number): string {
    if (id > this.categories.length || id == 0) {
      return 'brak kategorii';
    }

    return this.categories.filter(function (item) {
      return item.id === id;
    })[0].name;
  }

  private setMainImgSrc = (
    recipe: GetUserRecipeListItemModel,
    file: File | Blob
  ): void => {
    let myReader: FileReader = new FileReader();

    myReader.onloadend = function (e) {
      recipe.mainImageSrc = myReader.result.toString();
    };
    myReader.readAsDataURL(file);
  };

  onRecipeEdit = (recipeId: number): void => {
    this.router.navigate([`recipe/create-recipe/${recipeId}`]);
  };

  onRecipeDelete = (recipeId: number): void => {
    this.confirmRecipeDelete(recipeId);
  };

  private confirmRecipeDelete = (recipeId: number): void => {
    this.confirmationService.createConfirmBase(
      'usuń',
      'Przepis zostanie usunięty. Czy chcesz usunąć?',
      'Tak',
      'Nie',
      () => {
        this.deleteRecipe(recipeId);
      },
      () => {}
    );
  };

  private deleteRecipe = (recipeId: number): void => {
    this.loaderService.show();

    this.recipesService
      .deleteRecipe(recipeId)
      .pipe(
        finalize(() => {
          this.router.navigate([`home`]);
          this.loaderService.hide();
        })
      )
      .subscribe(
        (result) => {
          window.location.reload();
        },
        (error) => {}
      );
  };

  onUserDelete = (): void => {
    this.confirmUserDelete(this.authService.loggedId);
  };

  private confirmUserDelete = (userId: string): void => {
    this.confirmationService.createConfirmBase(
      'usuń',
      'Konto zostanie usunięte. Czy na pewno chcesz usunąć?',
      'Tak',
      'Nie',
      () => {
        this.deleteUser(userId);
      },
      () => {}
    );
  };

  private deleteUser = (userId: string): void => {
    this.loaderService.show();

    this.userService
      .deleteUser(userId)
      .pipe(
        finalize(() => {
          this.loaderService.hide();
        })
      )
      .subscribe(
        (result) => {
          this.authService.logOut();
        },
        (error) => {}
      );
  };
}
