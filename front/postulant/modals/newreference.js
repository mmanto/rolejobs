"use strict";

/**
 * Modal for new education
 * @memberof Postulant
 * @ngdoc service
 * @name PostulantNewReferenceModal
 */

const angular = require("angular");

const factory = function ($modal) {

    const modalCtl = [
        "$scope",
        "reference",
    function ($scope, reference) {

        $scope.referenceData = {};

        $scope.apiErrors = {
            referenceForm: {}
        };

        $scope.$watchCollection("referenceData", () => {
            $scope.apiErrors.referenceForm = {};    
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

            data = angular.copy($scope.referenceData);

            console.log("reference", data);

            $scope.$close(data);
            
        };
        
        $scope.cancel = function () {
            $scope.$dismiss('canceled');
        };

        if (reference) {
            $scope.referenceData = reference;
            angular.forEach($scope.referenceData, (v, k) => {
                if (typeof v === "number") {
                    $scope.referenceData[k] = v.toString();
                } 
            });
        }

    }];

    const open = function (data = null) {

        var modal = $modal.open({
            templateUrl: '/api/v1/postulant/templates/add_reference.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                reference() {
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
