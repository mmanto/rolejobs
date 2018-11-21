"use strict";

const jobTemplate = require("jobs/job.html");

/**
 * Job directive, the job item
 * @memberof Jobs
 * @ngdoc directive
 * @name jobItem
 */

const jobItem = function () {

    return {
        strict: "E",
        replace: true,
        template: jobTemplate,
        scope: {
            job:"="
        },

        controller: ["$scope", function($scope){

            $scope.favoritesrc = "/static/img/result-item-fav.svg";

            $scope.tooglefavorite = function(jobpk){

                if ($scope.favoritesrc == "/static/img/result-item-fav.svg")
                {
                    $scope.favoritesrc = "/static/img/result-item-red-fav.svg";
                }
                else{

                    $scope.favoritesrc = "/static/img/result-item-fav.svg";
                }

                console.log("toogle favorite for " + jobpk)
            };

        }]
    };

};

module.exports = jobItem;
