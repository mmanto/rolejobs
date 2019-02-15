"use strict";

const angular = require("angular");

/**
 * Employer panel controller
 * @memberof Employer 
 * @ngdoc controller
 * @name EmployerHomeCtl
 */

const factory = function ($q, $scope, EmployerService) {

    $scope.updateGlobalStats = function () {
        return EmployerService.getGlobalStats()
            .then((globalstats) => {
                $scope.globalstats = globalstats;
            });
    };

    $q.all([
        $scope.updateGlobalStats()
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "EmployerService",
    factory
];
