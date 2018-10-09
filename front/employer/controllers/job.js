"use strict";

/**
 * Job detail controller
 * @memberof Employer
 * @ngdoc controller
 * @name EmployerJobDetailCtl
 */

const factory = function ($q, $scope, $state, $params, JobsCollections,
                                                    PostulationsService) {

    const jobPk = $params.pk;
    const collection = JobsCollections.OwnJobs.getInstance();
    const pCollection = new PostulationsService.OwnJobPostulations(jobPk);
    
    $scope.actualPage = $params.page || 1;

    $scope.job = null;
    $scope.postulations = null;

    $scope.edit = function () {
        return $state.go("^.jobedit", {
            pk: jobPk
        });
    };

    $scope.view = function (pk) {
        $state.go("employer.main.jobpostulation", {
            jobPk,
            pk
        });
    };

    $scope.changePage = function (page = 1) {

        if (!$scope.postulations) {
            return;
        }

        return $state.go("^.job", {
            pk: jobPk,
            page: page
        });
    };

    $scope.updateJob = function () {
        collection.getItem(jobPk)
            .then((job) => {
                $scope.job = job;
            });
    };

    $scope.updatePostulations = function () {
        pCollection.fetch($scope.actualPage || 1)
            .then((postulations) => {
                $scope.postulations = postulations;
            });
    };

    return $q.all([
        $scope.updateJob(),
        $scope.updatePostulations(),
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$stateParams",
    "JobsCollections",
    "PostulationsService",
    factory
];
