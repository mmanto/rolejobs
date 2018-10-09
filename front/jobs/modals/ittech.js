"use strict";

/**
 * Modal for new tech requirement 
 * @memberof Jobs
 * @ngdoc service
 * @name ITTechModal 
 */

const angular = require("angular");

const factory = function ($modal) {

    const modalCtl = [
        "$q",
        "$scope",
        "TechsService",
        "requirement",
        "options",
    function ($q, $scope, TechsService, requirement, options) {

        $scope.requirementData = {};
        $scope.showExclusive = options.showExclusive || false;
        $scope.tech = {
            subtechnologies: []
        };

        $scope.apiErrors = {
            requirementForm: {}
        };

        $scope.$watchCollection("requirementData", () => {
            $scope.apiErrors.requirementForm = {};    
        });

        $scope.$watch("requirementData.technology", (id) => {
            $scope.requirementData.subtechnology = null;
            return TechsService.byId(id).then((tech) => {
                $scope.tech = tech;
            });
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

            data = angular.copy($scope.requirementData);

            data.subtechnology = data.subtechnology.id;

            var subTech = $scope.tech.subtechnologies
                .find(i => i.id === parseInt(data.subtechnology));

            if (!subTech) {
                console.log("Error, subtech??", $scope.requirementData,
                    $scope.tech);
                return;
            }

            data.techInfo = $scope.tech;
            data.subTechInfo = subTech;

            console.log("requirement", data);

            $scope.$close(data);
            
        };
        
        $scope.cancel = function () {
            $scope.$dismiss('canceled');
        };

        $scope.loadRequirement = function () {

            if (requirement) {
                $scope.requirementData = requirement;
                angular.forEach($scope.requirementData, (v, k) => {
                    if (typeof v === "number") {
                        $scope.requirementData[k] = v.toString();
                    } 
                });
            }

            return $q.resolve($scope.requirementData);
            
        };

        return $q.all(
            $scope.loadRequirement()
        );

    }];

    const open = function (data = null, options = {}) {

        var modal = $modal.open({
            templateUrl: 
                '/api/v1/jobs/templates/new_knowledge_requirement.html',
            controller: modalCtl,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'form-modal',
            resolve: {
                requirement() {
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
