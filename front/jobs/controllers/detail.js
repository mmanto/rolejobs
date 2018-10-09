"use strict";

/**
 * Job detail controller
 * @memberof Jobs
 * @ngdoc controller
 * @name JobDetailCtl
 */

const factory = function ($scope, $state, $sce, AlertModal, jobData) {

    const POSTULATION_STATUS = "postulation_status";

    console.log("Detail", jobData);
    $scope.jobData = jobData;

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

            cache = $sce.trustAsHtml($scope.jobData.description);

            return cache;
        };
    })();

    $scope.postulate = function () {
        if (jobData[POSTULATION_STATUS] !== null) {
            return AlertModal.open(
                "Ya tiene una postulación a este aviso."
            );
        }

        $state.go("jobs.postulate", {
            id: jobData.id
        });

    };

};

module.exports = [
    "$scope",
    "$state",
    "$sce",
    "AlertModal",
    "jobData",
    factory
];
