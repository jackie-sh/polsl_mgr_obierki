export class CreateRecipeModel {
  id: string | number;
  title: string;
  content: string;
  categoryId: number;
  shortDescription: string;
  mainImageId: number;

  constructor() {
    this.id = null;
  }
}
