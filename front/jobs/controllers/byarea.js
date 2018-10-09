"use strict";

const angular = require("angular");

const factory = function ($q, $scope, $state, $stateParams, JobsCollections,
                                                                        area) {

    const jobsCollection = new JobsCollections.ByArea(area.id);

    $scope.area = area;
    $scope.jobs = null;
    $scope.actualPage = $stateParams.page || 1; 
    $scope.filters = $stateParams.filters || {
        subareas: {}
    };

    if ($stateParams.toSubarea) {
        $scope.filters.subareas[$stateParams.toSubarea] = true;
    }

    $scope.$watch("filters", () => {
        $scope.updateJobs();
    }, true);

    $scope.changePage = function (pag) {
        return $state.go($state.$current, {
            area: area.slug,
            page: pag,
            filters: $scope.filters
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

    return $q.all(
        $scope.updateJobs()
    );

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$stateParams",
    "JobsCollections",
    "area",
    factory
];
