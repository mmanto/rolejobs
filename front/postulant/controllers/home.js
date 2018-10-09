"use strict";

/**
 * Postulant home page controller 
 * @memberof Postulants
 * @ngdoc controller 
 * @name PostulantHomeCtl
 * @param {service} $scope
 * @param {service} PostulantService
 */

const HomeCtl = function ($scope, PostulantService) {
    $scope.postulant = new PostulantService();

    $scope.postulant.getDetails()
        .then((details) => {
            $scope.details = details;
        });

};

module.exports = [
    "$scope",
    "PostulantService",
    HomeCtl
];
