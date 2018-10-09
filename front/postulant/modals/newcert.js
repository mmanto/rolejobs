"use strict";

/**
 * Modal for new certification
 * @memberof Postulant
 * @ngdoc service
 * @name PostulantNewCertificationModal
 */

const angular = require("angular");

const factory = function ($modal) {

    const modalCtl = [
        "$scope",
        "certification",
    function ($scope, certification) {

        $scope.certificationData = {};

        $scope.apiErrors = {
            certificationForm: {}
        };

        $scope.$watchCollection("certificationData", () => {
            $scope.apiErrors.certificationForm = {};    
        });

        $scope.dirtForm = function (form) {
            if (form.$error && form.$error.required) {
                form.$error.required.forEach((f) => {
                    f.$setDirty(); 
                });
            }

            return form;
        };

        $scope.save = function (form) {
            var data;

            $scope.dirtForm(form);

            if (form.$invalid) {
                return;
            }

            data = angular.copy($scope.certificationData);

            console.log("certification", data);

            $scope.$close(data);
            
        };
        
        $scope.cancel = function () {
            $scope.$dismiss('canceled');
        };

        if (certification) {
            $scope.certificationData = certification;
            angular.forEach($scope.certificationData, (v, k) => {
                if (typeof v === "number") {
                    $scope.certificationData[k] = v.toString();
                } 
            });
        }

    }];

    const open = function (data = null) {

        var modal = $modal.open({
            templateUrl: '/api/v1/postulant/templates/add_certification.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                certification() {
                    return data;
                }
            }
        });

        return modal;

    };

    return {
        open
    };

};

module.exports = [
    "$modal",
    factory 
];
