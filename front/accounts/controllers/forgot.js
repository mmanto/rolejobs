"use strict";

/**
 * Forgot password controller
 * @ngdoc controller
 * @name ForgotPasswordCtl
 * @memberof Account
 */

const factory = function ($scope, $state, alertModal, AccountService,
                                                        FormHelper) {

    $scope.formData = {
        email: "",
    };

    $scope.send = function send (form) {

        FormHelper.isValid(form)
            .then(() => {
                return AccountService.resetPassword($scope.formData.email);
            })
            .then(() => {
                return AccountService.verifyResetPasswordEmail($scope.formData.email);
            })
            .then(() => {
                $scope.formData.email = "";
                alertModal.open(
                    "Ya se ha enviado un correo a la dirección indicada " +
                    "siga los pasos del mismo para poder volver a ingresar " +
                    "a su cuenta"
                );
            })
            .then(() => {
                $state.go("home"); 
            })
            .catch(() => {
                return alertModal.open(
                    "Por favor, ingrese una direccion de correo válida y registrada.");
            });

    };


};

module.exports = [
    "$scope",
    "$state",
    "AlertModal",
    "AccountService",
    "FormHelper",
    factory
];
