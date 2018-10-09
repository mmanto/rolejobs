"use strict";

const angular = require("angular");

const factory = function ($q, $scope, $state, $stateParams, JobsCollections,
                            RolesSerive) {

    const jobsCollection = JobsCollections.WithRoles.getInstance();

    $scope.jobs = null;
    $scope.roles = [];
    $scope.actualPage = $stateParams.page || 1; 
    $scope.filters = $stateParams.filters || {
        roles: {}
    };

    $scope.$watch("filters", () => {
        $scope.updateJobs();
    }, true);

    $scope.changePage = function (pag) {
        return $state.go($state.$current, {
            page: pag,
            filters: $scope.filters
        });
    };

    $scope.updateRoles = function () {
        return RolesSerive.list()
            .then((roles) => {
                $scope.roles = roles;
            });
    };

    $scope.updateJobs = function () {

        var params = {};

        angular.forEach($scope.filters, (f, k) => {
            var items = [];

            angular.forEach(f, (v, kk) => {
                if (v === true) {
                    items.push(kk);
                }
            });

            if (items.length) {
                params[`filter_${k}`] = items.join(",");
            }
        
        });

        return jobsCollection.fetch($scope.actualPage, {params})
            .then((jobs) => {
                $scope.jobs = jobs;
            })
            .catch((err) => {
                if (err.status === 404) {
                    return $scope.changePage(1);
                }
            });

    };

    return $q.all([
        $scope.updateRoles(),
        $scope.updateJobs(),
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$stateParams",
    "JobsCollections",
    "RolesService",
    factory
];
