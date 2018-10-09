"use strict";

const factory = function ($q) {

    class ApiErrorsMannager {

        constructor (scope) {
            this._scope = scope;

            if (typeof this._scope.apiErrors !== "object") {
                this._scope.apiErrors = {};
            }

        }

        addWatcher (name, formName) {

            if (typeof formName === "undefined"){
                formName = `${name}Form`;
                name = `${name}Data`;
            }

            if (typeof this._scope.apiErrors[formName] !== "object") {
                this._scope.apiErrors[formName] = {};
            }

            var handler = this._scope.$watchCollection(name, () => {
                this._scope.apiErrors[formName] = {};    
            });

            this._scope.$on("$destroy", handler);

        }

        getApiErrors (form, data) {
            var errors = [];

            for (var i in data) {
                if (form[i]) {
                    form[i].$setDirty();
                    this._scope.apiErrors[form.$name][i] = {
                        msg: data[i][0]
                    };
                    errors.push({
                        field: i,
                        msgs: data[i]
                    });
                }
            }

            return errors;
       
        }

        displayErrors (form, data) {

            for (var i in data) {
                if (form[i]) {
                    form[i].$setDirty();
                    this._scope.apiErrors[form.$name][i] = {
                        msg: data[i][0]
                    };
                }
            }

        }
     
    }

    const dirty = (form) => {

        if (form.$error && form.$error.required) {
            form.$error.required.forEach((f) => {
                f.$setDirty(); 
            });
        }

        return form;

    };

    const isValid = (form) => {
        return $q((resolve, reject) => {
            dirty(form);
            if (form.$invalid) {
                return reject(form.$error);
            } else {
                return resolve(form);
            }
        });
    };

    const reset = (form) => {
        if (form) {
            form.$setPristine();
            form.$setUntouched();
        }
    };

    return {
        ApiErrorsMannager,
        dirty,
        isValid,
        reset,
    };

};

module.exports = [
    "$q",
    factory
];
