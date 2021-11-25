import { NgModule } from '@angular/core';
import { Routes, RouterModule, Route } from "@angular/router";
import { HomeComponent } from './views/home/home.component';


const routes: Route[] = [
  {
    path: "home",
    component: HomeComponent,
    data: {
      title: "Strona główna",
      breadcrumbs: "Strona główna",
    },
  },
  {
    path: "auth",
    loadChildren: () => 
    import("./views/auth/auth.module").then((m) => m.AuthModule),
    data: {
      title: "Logowanie i rejestracja",
      breadcrumbs: null,
    },
  },
  {
    path: "",
    redirectTo: "home",
    pathMatch: "full",
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
