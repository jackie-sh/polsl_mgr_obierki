export class AppHelper {
  static getBaseUrl() {
    return document.getElementsByTagName("base")[0].href;
  }
}