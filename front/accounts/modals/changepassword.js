"use strict";

/**
 * Modal for password change 
 * @memberof Accounts
 * @ngdoc service
 * @name ChangePasswordModal
 *
 */

const factory = function ($modal) {

    const modalCtl = [
        "$scope",
        "AlertModal",
        "FormHelper",
        "AccountService",
    function ($scope, $alert, FormHelper, AccountService) {

        $scope.changePasswordData = {
            "old_password": "",
            "new_password1": "",
            "new_password2": ""
        };

        $scope.apiErrors = {};

        $scope.apiErrors = {
            changePasswordForm: {}
        };

        const formManager = new FormHelper.ApiErrorsMannager($scope);

        formManager.addWatcher("changePassword");

        $scope.save = function (form) {
            return FormHelper.isValid(form)
                .then(() => {
                    return AccountService.changePassword(
                        $scope.changePasswordData); 
                })
                .then(() => {
                    return $alert.open("Contraseña cambiada con exito",
                        "Cambio realizado"); 
                })
                .then(() => {
                    return $scope.$close();
                })
                .catch((response) => {
                    if (response.data) {
                        formManager.displayErrors(form, response.data);
                    } else {
                        return $alert.open(
                            "Ha habido un error al procesar su pedido, " + 
                            "reintente."); 
                    }
                });
        };

    }];

    const open = function () {

        var modal = $modal.open({
            templateUrl: '/api/v1/accounts/templates/change_password.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal change-password-modal',
        });

        return modal;

    };

    return {
        open
    };

};

module.exports = [
    "$modal",
    factory
];
