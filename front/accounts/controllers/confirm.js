"use strict";

module.exports = [
    "$scope",
    "$modal",
    "$stateParams",
    "$state",
    "AccountService",
function ($scope, $modal, $stateParams, $state, AccountService) {

    var id = $stateParams.id;
    var hash = $stateParams.hash;

    console.log($stateParams);

    $scope.confirm = function () {
        AccountService.confirmAccount({id, hash})
            .then((success) => {
                if (success) {
                    $state.go("accounts.login");
                } else {
                    throw new Error("Not success");
                }
            })
            .catch((e) => {
                $modal.open({
                    template: e.toString()
                });
            });
    };


}];
