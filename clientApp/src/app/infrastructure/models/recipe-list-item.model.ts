export class RecipeListItemModel {
    id: string | number;
    title: string;
    description: string;
    categoryId: string | number;
    category: string;
    createdDate: Date;
    mainImageId: string;
    mainImageSrc: string;
    rating: number;
  }