"use strict";

/**
 * Contact controller
 * @memberof Home
 * @ngdoc controller
 * @name ContactCtl
 */

const factory = function ($scope, AlertModal, ApiService) {

    const NON_FIELD_ERRORS = "non_field_errors";

    $scope.contactData = {};

    $scope.apiErrors = {
        contactForm: {}
    };

    $scope.$watchCollection("contactData", () => {
        $scope.apiErrors.contactForm = {};    
    });

    $scope.dirtForm = function (form) {
        if (form.$error && form.$error.required) {
            form.$error.required.forEach((f) => {
                f.$setDirty(); 
            });
        }

        return form;
    };

    $scope.displayApiErrors = function (form, data) {

        if (data[NON_FIELD_ERRORS]) {
            $scope.apiErrors[form.$name].$nonfield = {
                msg: data[NON_FIELD_ERRORS][0]
            };
        }

        for (var i in data) {
            if (form[i]) {
                form[i].$setDirty();
                // form.$setValidity(i, false);
                $scope.apiErrors[form.$name][i] = {
                    msg: data[i][0]
                };
            }
        }
    };

    $scope.reset = function(form) {
        $scope.apiErrors.contactForm = {}; 
        $scope.contactData = {};
        form.$setUntouched();
        form.$setPristine();
    };

    $scope.send = function (form) {
        $scope.dirtForm(form);

        if (form.$invalid) {
            return;
        }

        ApiService.getInstance().post(`contact/`, $scope.contactData)
            .then(() => {
                $scope.reset(form);
                AlertModal.open(
                    "Su mensaje ha sido enviado, en breve nos estaremos " +
                    "comunicando con usted.",
                    "Mensaje enviado"
                );
            })
            .catch((response) => {
                if (response.data) {
                    $scope.displayApiErrors(form, response.data);
                } else {
                    $scope.displayApiErrors(form, {
                        "non_field_errors": ["Error al enviar el mensaje," + 
                                          " por favor vuelva a intentanrlo"]
                    });
                }
            });
         
    };

};

module.exports = [
    "$scope",
    "AlertModal",
    "Apiv1Service", 
    factory
];
