"use strict";

const factory = function ($scope, CoursesService) {

    
    $scope.courses = [];

    $scope.filters = {
        query: "",
    };


    $scope.updateCourses = function () {
        return CoursesService.getCourses()
            .then((courses) => {
                $scope.courses = courses;
            });
    };

};

module.exports = [
    "$scope",
    "CoursesService",
    factory
];
