import { CommentModel } from './comment.model';

export class GetRecipeModel {
  title: string;
  content: string;
  authorName: string;
  recipeId: number;
  authorId: number;
  createdDate: Date;
  rating: number;
  shortDescription: string;
  views: number;
  comments: CommentModel[];

  constructor() {
    this.comments = [];
  }
}
