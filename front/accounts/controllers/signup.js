"use strict";

const FORMATED_ADDRESS = "formatted_address";

module.exports = [
    "$scope",
    "$state",
    "$modal",
    "PostulantService",
    "$window",
function ($scope, $state, $modal, PostulantService,$window) {

    $scope.address = null;

    $scope.formData = {
        firstName: "",
        lastName: "",
        city: "",
        email: "",
        password: ""
    };

    $scope.errors = {};

    $scope.signup = function () {
        console.log("Signup", $scope.formData);

        $scope.errors = {};

        if ($scope.address) {
            $scope.formData.city = $scope.address;
        }

        PostulantService.getInstance().signup($scope.formData)
            .then((result) => {
                console.log(result);

                $state.go("accounts.confirmationsent", {
                    email: result.email
                });
            })
            .catch((result) => {
                console.log("Error " + result.code);

                if (result.data) {
                    $scope.errors = result.data;
                }

            });

    };

    $scope.placeChanged = function () {
        var place = this.getPlace();
        $scope.address = place[FORMATED_ADDRESS];
        console.log($scope.address);
    };

    $scope.facebook = function () {
            $state.go("accounts.facebook");
            $window.location.reload();
    };

    $scope.google = function () {
            console.log("Entro en google");
            $state.go("accounts.google");
            $window.location.reload();
    };

    $scope.linkedin = function () {
        console.log("Link a linkedin");
        $state.go("accounts.linkedin");
        $window.location.reload();
    };

}];
