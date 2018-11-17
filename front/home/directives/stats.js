"use strict";

/**
 * Profile avatar image
 * @memberof Home
 * @ngdoc directive
 * @name statsData
 */

const statsData = function () {
    return {
        strict: "E",
        replace: true,
        scope: {
            jobsLabel: "@",
            postulationsLabel: "@",
            enterpricesLabel: "@"
        },
        template: `<div class="row" style="text-align:center; color:darkgray" >
        <div class="small-4 large-4 columns" > <span style="color:navy" > {{ jobsCount }}</span>  {{ jobsLabel }} </div>
        <div class="small-4 large-4 columns" > <span style="color:navy">{{ postulationsCount }}</span> {{ postulationsLabel }} </div>
        <div class="small-4 large-4 columns" > <span style="color:navy">{{ enterpricesCount }}</span> {{ enterpricesLabel }} </div>
      </div>`,
        controller: ["$scope", 
                "Apiv1Service",
                ($scope, Apiv1Service) => {
                    Apiv1Service.getInstance().get("stats")
                    .then((response)=>{

                        $scope.jobsCount = response.data.jobs;

                        $scope.postulationsCount = response.data.postulations;

                        $scope.enterpricesCount = response.data.enterprices;

                    });

                }
            ]
        
    };

};

module.exports = statsData;