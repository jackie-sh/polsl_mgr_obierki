export class CreateRecipeModel {
    id: string | number;
    title: string;
    content: string;
    categoryId: number;
    mainImageId: string;
  
    constructor() {
      this.id = null;
    }
  }
  