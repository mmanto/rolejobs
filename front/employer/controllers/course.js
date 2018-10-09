"use strict";

/**
 * Course detail controller
 * @memberof Employer
 * @ngdoc controller
 * @name EmployerCourseDetailCtl
 */

const factory = function ($q, $scope, $state, $params,CoursesCollections) {

    const coursePk = $params.pk;
    const collection = CoursesCollections.OwnCourses.getInstance();
    //const pCollection = new PostulationsService.OwnCoursePostulations(coursePk);
    
    $scope.actualPage = $params.page || 1;

    $scope.course = null;
    $scope.postulations = null;

    $scope.edit = function () {
        return $state.go("^.courseedit", {
            pk: coursePk
        });
    };

    $scope.view = function (pk) {
        $state.go("employer.main.coursepostulation", {
            coursePk,
            pk
        });
    };

    $scope.changePage = function (page = 1) {

        if (!$scope.postulations) {
            return;
        }

        return $state.go("^.course", {
            pk: coursePk,
            page: page
        });
    };

    $scope.updatecourse = function () {
        collection.getItem(coursePk)
            .then((course) => {
                $scope.course = course;
            });
    };

    /*$scope.updatePostulations = function () {
        pCollection.fetch($scope.actualPage || 1)
            .then((postulations) => {
                $scope.postulations = postulations;
            });
    };*/

    return $q.all([
        $scope.updatecourse()
        //$scope.updatePostulations(),
    ]);
    
};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$stateParams",
    "CoursesCollections",
    factory
];
