"use strict";

module.exports = [
    "$scope",
    "$modal",
    "$state",
    "$window",
    "$timeout",
    "AlertModal",
    "AccountService",
function ($scope, $modal, $state, $window, $timeout, $alert, AccountService) {

    $scope.formData = {
        email: "",
        password: ""
    };

    $scope.login = function () {

        AccountService.login($scope.formData)
            .then(() => {
                $state.go("home", {}, {
                    reload: true
                }).then(() => {
                    $window.location.reload();
                });
            })
            .catch(() => {
                $alert.open(
                    "Contraseña o email incorrectos, verifique que " +
                    "sean correctos, y reintente.");
            });

    };
}];
