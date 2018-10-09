"use strict";

const factory = function ($q, $scope, AreasService, JobsService) {

    $scope.areas = [];
    $scope.jobs = [];

    $scope.filters = {
        query: "",
        areas: {} 
    };

    $scope.updateAreas = function () {
        return AreasService.list()
            .then((areas) => {
                $scope.areas = areas;
            });
    };

    $scope.updateJobs = function () {
        return JobsService.getJobs()
            .then((jobs) => {
                $scope.jobs = jobs;
            });
    };

    return $q.all(
        $scope.updateAreas()
    );

};

module.exports = [
    "$q",
    "$scope",
    "AreasService",
    "JobsService",
    factory
];
