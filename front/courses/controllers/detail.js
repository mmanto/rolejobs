"use strict";

/**
 * Course detail controller
 * @memberof Courses
 * @ngdoc controller
 * @name CourseDetailCtl
 */

const factory = function ($scope, $state, $sce, AlertModal, courseData) {

    const POSTULATION_STATUS = "postulation_status";

    console.log("Detail", courseData);
    $scope.courseData = courseData;

    $scope.postulationStatus = {
        0x00: {
            type: "info",
            message: "Estás postulado a este aviso," + 
                     " aún está en espera de respuesta"
        },
        0x10: {
            type: "success",
            message: "Han aceptado tu postulación a este aviso"
        },
        0x20: {
            type: "alert",
            message: "Tu postulación a este aviso ha sido rechazada"
        }
    };

    $scope.getDescription = (function () {
        var cache = null;

        return function (force = false) {
            if (!force && cache) {
                return cache;
            }

            cache = $sce.trustAsHtml($scope.courseData.description);

            return cache;
        };
    })();

    $scope.postulate = function () {
        if (courseData[POSTULATION_STATUS] !== null) {
            return AlertModal.open(
                "Ya tiene una postulación a este aviso."
            );
        }

        $state.go("courses.postulate", {
            id: courseData.id
        });

    };

};

module.exports = [
    "$scope",
    "$state",
    "$sce",
    "AlertModal",
    "courseData",
    factory
];
