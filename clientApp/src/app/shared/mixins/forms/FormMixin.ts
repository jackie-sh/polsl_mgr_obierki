import { Constructor } from "@angular/material/core/typings/common-behaviors/constructor";
import { FormGroup } from "@angular/forms";

/**
 * Mixin for handle forms. Validates inputs, builds error messages, allows override method to execute forms action
 * @param Base component class where exist form which should be served.
 *
 */
export function FormMixin<T extends Constructor<{}>>(
  Base: T = class {} as any
) {
  return class extends Base {
    /**
     * The form to be handled
     * */
    public form: FormGroup;
    /**
     * The key-value object or array of values used to display correct name of invalid input
     * */
    protected displayNames: any;
    protected errorMessages: ErrorMessageMap = {};
    private readonly defaultErrorText: string = "Błąd w polu ";
    private isSubmited: boolean = false;

    /**
     * The method that starts handling the form
     * */
    onSubmit = (): void => {
      this.isSubmited = true;
      if (this.isValid) this.validationSuccess(this.form.value);
      else this.validationFailure();
    };

    /**
     * Returns true if all inputs are filled correct
     * */
    get isValid(): boolean {
      this.form.markAllAsTouched();
      return this.form.valid;
    }

    /**
     * Return true if input is filled incorrect
     * */
    hasError = (fieldName: string): boolean => {
      const field = this.form.controls[fieldName];
      return field.touched && field.invalid && this.isSubmited;
    };

    /**
     * Return errors form all inputs
     * */
    get errors() {
      const result: any[] = [];
      Object.keys(this.form.controls).forEach((key) => {
        result.push(...this.collectErrors(key));
      });

      return result;
    }

    /**
     * Return array with first error model for form field
     * @param{string} fieldName key of form property
     * */
    public collectErrors = (
      fieldName: string
    ): { fieldName: string; errorMessage: string }[] => {
      const field = this.form.get(fieldName);

      if (this.isSubmited && field.touched && field.errors) {
        const result = Object.keys(field.errors)
          .slice(0, 1)
          .map((key) => {
            return {
              fieldName: fieldName,
              errorMessage: this.getErrorMessage(
                this.errorMessages[`${fieldName}${key}`] ||
                  this.errorMessages[key],
                this.getDisplayName(fieldName)
              ),
            };
          });
        return result;
      } else return [];
    };

    /**
     * Builds the error message based on the arguments passed
     * @param{string} displayName the value witch is replaced from default field name
     *
     * */
    private getErrorMessage = (
      f: (...args: string[]) => string,
      displayName: string
    ): string => {
      if (f) return f(displayName);
      return `${this.defaultErrorText}${displayName}`;
    };

    /**
     * Returns display name value if exist in displayNames object else returns provided param
     * @param{string} fieldName key of displayNames property
     * */
    private getDisplayName = (fieldName: string): string => {
      return this.displayNames[fieldName]
        ? this.displayNames[fieldName]
        : fieldName;
    };

    /**
     * Hook for action which is called after successed validation. ( Should be overridden in the inheriting class )
     * @param{any} formValueObject object which contain values of inputs
     * */
    protected validationSuccess = (formValueObject): void => {
      //hook
    };

    /**
     * Hook for action which shoud be call after seccessed validation ( Should be overridden in the inheriting class )
     * */
    protected validationFailure = (): void => {
      //hook
    };
  };
}

export interface ErrorMessageMap {
  [validationName: string]: (...args: string[]) => string;
}
