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
            usersLabel: "@",
            employersLabel: "@"
        },
        template: `<div class="row" style="text-align:center; color:darkgray" >
        <div class="small-4 large-4 columns"> 
            <span style="color:navy" > {{ jobsCount }}</span> 
            <img src="/static/img/jobs-stats-icon.png" /> 
            <span> {{ jobsLabel }} </span> 
        </div>
        <div class="small-4 large-4 columns"> 
            <span style="color:navy">{{ usersCount }}</span> 
            <img src="/static/img/users-stats-icon.png" /> 
            <span> {{ usersLabel }} </span> 
        </div>
        <div class="small-4 large-4 columns">
            <span style="color:navy">{{ employersCount }}</span>  
            <img src="/static/img/employers-stats-icon.png" />
            <span> {{ employersLabel }} </span>
        </div>
        
      </div>`,
        controller: ["$scope", 
                "Apiv1Service",
                ($scope, Apiv1Service) => {
                    Apiv1Service.getInstance().get("stats")
                    .then((response)=>{

                        $scope.jobsCount = response.data.jobs;

                        $scope.usersCount = response.data.users;

                        $scope.employersCount = response.data.employers;

                    });

                }
            ]
        
    };

};

module.exports = statsData;