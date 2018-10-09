"use strict";

/**
 * Complete profile directive 
 * @memberof Postulant
 * @ngdoc directive
 * @name postulantCompleteProfile
 */

const template = require("postulant/completed-profile.html");

const IS_COMPLETED = "is_completed";

const factory = function () {

    return {
        restrict: "E",
        replace: true,
        template,
        scope: {
            data: "="
        },
        controller: [
            "$scope",
            ($scope) => {

                const postStart = 100;
                const postTotal = 92;

                const getPostRest = function (percent) {
                    var rest = percent * postTotal / 100;
                    return postStart - rest;
                };

                $scope.percent = 0;
                $scope.restItems = [];
                $scope.itemPercent = 0;

                $scope.$watchCollection("data", (newValue) => {

                    if (!newValue) {
                        return;
                    }
                                        
                    $scope.percent = newValue.percent || 0;
                    $scope.overlayPos = getPostRest($scope.percent);

                    if (newValue.items) {
                        var notComplete =  newValue.items
                            .filter(x => !x[IS_COMPLETED]);

                        $scope.itemPercent = Math.round(
                            100 / newValue.items.length);
                        
                        $scope.restItems = notComplete.slice(0, 2);
                    }

                });

            }
        ]
    };

};

module.exports = factory;
