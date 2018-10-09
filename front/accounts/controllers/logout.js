"use strict";

const logoutController = function (
                          $scope, $timeout, $state, $window, AccountService) {

    $scope.logout = function () {
        console.log("log out");
        AccountService.logout()
            .then(() => {
                $state.go("home");
                $timeout(() => {
                    $window.location.reload();
                }, 400);
           });
    };

};

module.exports = [
    "$scope",
    "$timeout",
    "$state",
    "$window",
    "AccountService",
    logoutController
];
