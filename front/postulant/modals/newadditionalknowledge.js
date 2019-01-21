"use strict";

/**
 * Modal for new language
 * @memberof Postulant
 * @ngdoc service
 * @name PostulantNewAdditionalknowledgeModal
 */

const angular = require("angular");

const factory = function ($modal) {

    const modalCtl = [
        "$scope",
        "PostulantService",
        "additionalknowledge",
        "options",
    function ($scope, PostulantService, additionalknowledge, options) {

        const NON_FIELD_ERRORS = 'non_field_errors';

        $scope.blockAdditionalknowledge = false;

        $scope.additionalknowledgeData = {
            
        };

        $scope.apiErrors = {
            additionalknowledgeForm: {}
        };

        $scope.$watchCollection("additionalknowledgeData", () => {
            $scope.apiErrors.additionalknowledgeForm = {};    
        });

        $scope.requestExclusive = options.exclusive || false;

        $scope.dirtForm = function (form) {
            if (form.$error && form.$error.required) {
                form.$error.required.forEach((f) => {
                    f.$setDirty(); 
                });
            }

            return form;
        };

        $scope.displayApiErrors = function (form, data) {

            if (data[NON_FIELD_ERRORS]) {
                $scope.apiErrors[form.$name].$nonfield = {
                    msg: data[NON_FIELD_ERRORS][0]
                };
            }

            for (var i in data) {
                if (form[i]) {
                    form[i].$setDirty();
                    // form.$setValidity(i, false);
                    $scope.apiErrors[form.$name][i] = {
                        msg: data[i][0]
                    };
                }
            }
        };

        $scope.save = function (form) {
            var data;

            $scope.dirtForm(form);

            if (form.$invalid) {
                return;
            }

            data = angular.copy($scope.additionalknowledgeData);

            if (options.nosave) {
                return $scope.$close(data);
            }

            PostulantService.getInstance().saveAdditionalknowledge(data)
                .then((data) => {
                    $scope.$close(data);
                })
                .catch((err) => {
                    if (err.data) {
                        $scope.displayApiErrors(form, err.data);
                    }
                });

        };
        
        $scope.cancel = function () {
            $scope.$dismiss('canceled');
        };

        if (additionalknowledge) {
            $scope.blockAdditionalknowledge = true;
            $scope.additionalknowledgeData = additionalknowledge;
            angular.forEach($scope.additionalknowledgeData, (v, k) => {
                if (typeof v === "number") {
                    $scope.additionalknowledgeData[k] = v.toString();
                } 
            });
        }

    }];

    const open = function (data = null, options = {}) {

        var modal = $modal.open({
            templateUrl: '/api/v1/postulant/templates/add_additionalknowledge.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                additionalknowledge() {
                    return data;
                },
                options() {
                    return options;
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
