"use strict";

/**
 * Password reset controller
 * @memberof Accounts
 * @ngdoc controller
 * @name ResetPasswordCtl
 */

const NEW_PASSWORD1 = "new_password1";
const NEW_PASSWORD2 = "new_password2";

const factory = function ($scope, $params, FormHelper, $alert, $aealert, $state,
                                                            AccountService) {

    const {uid, token} = $params;

    const fieldTable = {
        "new_password1": "Contraseña",
        "new_password2": "Contraseña"
    };
   
    $scope.resetPasswordData = {
        "new_password1": "",
        "new_password2": ""
    };
    
    $scope.apiErrors = {};

    $scope.uid = $params.uid;
    $scope.token = $params.token;

    const formManager = new FormHelper.ApiErrorsMannager($scope);

    formManager.addWatcher("resetPassword");

    $scope.send = function (form) {
        return FormHelper.isValid(form)
            .then(() => {
                var password1 = $scope.resetPasswordData[NEW_PASSWORD1];
                var password2 = $scope.resetPasswordData[NEW_PASSWORD2];

                if (password1 !== password2) {
                    throw new Error("Password don't match");
                }
                return password2;
            })
            .then((password) => {
                return AccountService.confirmResetPassword(
                    uid, token, password);
            })
            .then(() => {
                return $alert.open("Su contraseña ha sido actualizada " +
                                   "con exito");
            })
            .then(() => {
                return $state.go("accounts.login");
            })
            .catch((response) => {

                if (response.data && (response.data.token ||
                                                    response.data.uid)) {
                    return $alert.open(
                        "Este token está expirado o no es válido")
                        .then(() => {
                            $state.go("accounts.forgot");
                        });
                } else if (response.data) {
                    var errors = formManager.getApiErrors(form, response.data);
                    return $aealert.open(errors, fieldTable);
                } else {
                    console.log("Err", response);
                    return $alert.open(
                        "Ha habido un error al procesar su pedido, " + 
                        "reintente."); 
                }

            });
    };

};

module.exports = [
    "$scope",
    "$stateParams",
    "FormHelper",
    "AlertModal",
    "ApiErrorsAlertModal",
    "$state",
    "AccountService",
    factory
];
