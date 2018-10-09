"use strict";

/**
 * Postulant controller
 * @memberof postulants 
 * @ngname controller
 * @name PostulantCtl
 * @param {service} $scope
 */

const postulantCtl = function ($scope, $state) {
    $scope.tab = $state.current.data.tab;

    var stateChangeHandler = $scope.$on("$stateChangeSuccess", () => {
        $scope.tab = $state.current.data.tab;
    });

    $scope.$on("$destroy", stateChangeHandler);

};

module.exports = [
    "$scope",
    "$state",
    postulantCtl
];
