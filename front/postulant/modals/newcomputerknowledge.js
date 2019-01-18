"use strict";

/**
 * Modal for new language
 * @memberof Postulant
 * @ngdoc service
 * @name PostulantNewComputerknowledgeModal
 */

const angular = require("angular");

const factory = function ($modal) {

    const modalCtl = [
        "$scope",
        "PostulantService",
        "computerknowledge",
        "options",
    function ($scope, PostulantService, computerknowledge, options) {

        const NON_FIELD_ERRORS = 'non_field_errors';

        $scope.blockComputerknowledge = false;

        $scope.computerknowledgeData = {
            level: 0
        };

        $scope.apiErrors = {
            computerknowledgeForm: {}
        };

        $scope.$watchCollection("computerknowledgeData", () => {
            $scope.apiErrors.computerknowledgeForm = {};    
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

            data = angular.copy($scope.computerknowledgeData);

            if (options.nosave) {
                return $scope.$close(data);
            }

            PostulantService.getInstance().saveComputerknowledge(data)
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

        if (computerknowledge) {
            $scope.blockComputerknowledge = true;
            $scope.computerknowledgeData = computerknowledge;
            angular.forEach($scope.computerknowledgeData, (v, k) => {
                if (typeof v === "number") {
                    $scope.computerknowledgeData[k] = v.toString();
                } 
            });
        }

    }];

    const open = function (data = null, options = {}) {

        var modal = $modal.open({
            templateUrl: '/api/v1/postulant/templates/add_computerknowledge.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                computerknowledge() {
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
