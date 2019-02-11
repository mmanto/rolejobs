"use strict";

/**
 * Modal for new language
 * @memberof Postulant
 * @ngdoc service
 * @name PostulantNewWorkpreference
 */

const angular = require("angular");

const factory = function ($modal) {

    const modalCtl = [
        "$scope",
        "PostulantService",
        "workpreference",
        "options",
    function ($scope, PostulantService, workpreference, options) {

        const NON_FIELD_ERRORS = 'non_field_errors';

        $scope.blockWorkpreference = false;

        $scope.workpreferenceData = {
            
        };

        $scope.apiErrors = {
            workpreferenceForm: {}
        };

        $scope.$watchCollection("workpreferenceData", () => {
            $scope.apiErrors.workpreferenceForm = {};    
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

            data = angular.copy($scope.workpreferenceData);

            if (options.nosave) {
                return $scope.$close(data);
            }

            PostulantService.getInstance().saveWorkpreference(data)
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

        if (workpreference) {
            $scope.blockWorkpreference = true;
            $scope.workpreferenceData = workpreference;
            angular.forEach($scope.workpreferenceData, (v, k) => {
                if (typeof v === "number") {
                    $scope.workpreferenceData[k] = v.toString();
                } 
            });
        }

    }];

    const open = function (data = null, options = {}) {

        var modal = $modal.open({
            templateUrl: '/api/v1/postulant/templates/add_workpreference.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                workpreference() {
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
