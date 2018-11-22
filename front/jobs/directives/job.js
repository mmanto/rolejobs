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

        controller: ["$scope", "Apiv1Service", function($scope, Apiv1Service){
            
            if ($scope.job.usefavorite)
            {
                
                if ($scope.job.hasfavoritejob)
                {
                    $scope.favoritesrc = "/static/img/result-item-red-fav.svg";
                }
                else
                {
                    $scope.favoritesrc = "/static/img/result-item-fav.svg";
                }

            }
            

            $scope.tooglefavorite = function(){

                Apiv1Service.getInstance().post("jobs/setfavoritejob",
                        { 'pk': $scope.job.pk, 'favorite': !$scope.job.hasfavoritejob })
                        .then((response)=>{

                            if (response.data.success)
                            {
                                $scope.job.hasfavoritejob = !$scope.job.hasfavoritejob;
                                if ($scope.job.hasfavoritejob)
                                {
                                    $scope.favoritesrc = "/static/img/result-item-red-fav.svg";
                                }
                                else
                                {
                                    $scope.favoritesrc = "/static/img/result-item-fav.svg";
                                }


                            }
                            
                        });


            };

        }]
    };

};

module.exports = jobItem;
