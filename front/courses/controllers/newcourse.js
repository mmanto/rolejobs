"use strict";

/**
 * New course modal controller
 * @memberof courses
 * @ngdoc controller
 * @name NewCourseCtl
 */

const angular = require("angular");
const cancelModalTemplate = require("courses/course_cancel.html");

const getFakeId = (function () {
    var last = 0;

    return function () {
        last--;
        return last;
    };

})();

const factory = function ($q, 
                          $scope, 
                          $state, 
                          $stateParams,
                          $modal,
                          ConfirmModal, 
                          AlertModal, 
                          CoursesService,
                          meData) {


    $scope.courseData =  {
        "title": "",
        "description": "",
        "price": null,
        "currency_type": null,
        "course_type": 0,
        "notify_by_email": null
    };

    $scope.courseGeoData = null;

    $scope.lastcourses = [];

    $scope.isNew = true;

    $scope.pk = null;

    $scope.req = {};

    $scope.selected = {
        requirements: []
    };

    var qmodal;

    $scope.apiErrors = {
        courseForm: {}
    };


    $scope.addRequirement = function () {
        $scope.courseData.requirements.push({
            id: getFakeId(),
            description: $scope.req.description
            //exclusive: $scope.req.exclusive || false
        });
        $scope.req = {};
    };


    $scope.cancel = function (definitive = false) {

        if (definitive) {
            console.log("Cancel!!");

            if (qmodal) {
                qmodal.close();
            }

            $state.go("employer.main.courses");
            return;
        }

        qmodal = $modal.open({
            template: cancelModalTemplate,
            scope: $scope,
            backdrop: true
        });

    };

    $scope.error = function (err) {
        console.log(":(", err);
       
        if ($scope.courseForm.$error.required) {
            $scope.courseForm.$error.required.forEach((f) => {
                f.$setDirty();
            });
        }

        if (err.status >= 500 && err.status <= 599) {
            return AlertModal.open(
                "Ha habido un problema al procesar su publicación, por " +
                "favor, reintente."
            );
        }

        if (err && err.data && typeof err.data === "object") {
            for (var i in err.data) {

                if (!i.match(/^\w/i)) {
                    continue;
                }

                $scope.apiErrors.courseForm[i] = {
                    msg: err.data[i][0]
                };
                $scope.courseForm.$setValidity(i, false);
            }

        }

        AlertModal.open(
            "Verifique los datos e intente de nuevo",
            "El formulario contiene errores"
        );

    };

    $scope.success = function (result) {
        console.log("yea", result);
        if (qmodal) {
            qmodal.close();
        }
        $state.go("employer.main.courses");
    };

    $scope.prepareData = function () {
        var data = angular.copy($scope.courseData);

        if ($scope.pk) {
            data.pk = $scope.pk;
        }

        if ($scope.courseGeoData) {
            data.address = $scope.courseGeoData.address;
            data.country = $scope.courseGeoData.country;
            data.region = $scope.courseGeoData.region;
            data.city = $scope.courseGeoData.city;
        }


   
        return data;
    };

    $scope.save = function () {
        
        if ($scope.courseForm.$invalid) {
            return $scope.error();
        }

        var data = $scope.prepareData();
        
        CoursesService.saveCourse(data)
            .then($scope.success)
            .catch($scope.error);

    };

    $scope.draft = function () {

        if ($scope.courseForm.$invalid) {
            return $scope.error();
        }

        var data = $scope.prepareData();

        CoursesService.saveDraft(data)
            .then($scope.success)
            .catch($scope.error);
    };

    $scope.setCourse = function (course, asNew = false) {

        if (asNew) {
            $scope.isNew = true;
            delete course.id;
            delete course.pk;
        } else {
            $scope.isNew = false;
            $scope.pk = course.pk;
        }

        $scope.courseData = course;
        $scope.pk = course.pk;

        angular.forEach($scope.courseData, (v, k) => {

            if (k === "reference_number") {
                return;
            }

            if (typeof v === "number") {
                $scope.courseData[k] = v.toString();
            } 

        });


        if (course.geo) {
            $scope.courseGeoData = {
                address: course.geo.address,
                country: course.geo.country,
                region: course.geo.region,
                city: course.geo.city
            };

            delete course.address;
            delete course.country;
            delete course.region;
            delete course.city;

        } else {
            $scope.courseGeoData = {};
        }

        return course;

    };

    $scope.cloneFrom = function (courseId, form) {

        $q.when((() => {

            if (form.$dirty) {
                return ConfirmModal.open(
                    "Hay una edición en proceso, esto pisará todos los" + 
                    " campos, ¿está seguro de continuar?");
            } 

            return true;

        })()).then(() => {
            CoursesService.getOwnOne(courseId)
                .then((j) => $scope.setCourse(j, true));
        });

    };

    $scope.loadcourse = function() {

        return $q.when($stateParams.pk !== "-1", (arecourse) => {

            if (!arecourse) {

                // If the course is new course, set the same geo data than employer
                if (!$scope.courseGeoData) {
                    $scope.courseGeoData = {
                        address: meData.address,
                        country: meData.country,
                        region: meData.region,
                        city: meData.city,
                    };
                }

                return null;
            }

            $scope.isNew = false;

            return CoursesService.getOwnOne($stateParams.pk)
                .then($scope.setCourse);
        });

    };


/*
    CoursesService.getOwnLasts()
        .then((list) => {
            $scope.lastcourses = list;
        });
*/

    return $q.all([
        $scope.loadcourse()
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$stateParams",
    "$modal",
    "ConfirmModal",
    "AlertModal",
    "CoursesService",
    "me",
    factory
];