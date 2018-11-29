"use strict";

/**
 * Home controller
 * @memberof Home
 * @ngdoc controller
 * @name HomeCtl
 * @param {service} $scope
 * @param {service} JobsService
 * @param {service} CoursessService
 */ 

const factory = function ($q, $scope, $state, $http, JobsCollections, CoursesCollections,AreasService,
    RolesService, Apiv1Service, GeoService, EmployerService) {

    const jobsCollection = JobsCollections.PublicJobs.getInstance();
    
    const coursesCollection = CoursesCollections.PublicCourses.getInstance();

    $scope.jobs = null; 
    $scope.areas = [];
    $scope.roles = [];
    $scope.availableRoles = [];

    $scope.locations = [];

    $scope.courses = null; 

    $scope.companies = null;

    $scope.tags = [
    ];

    $scope.search = function () {
        let roles = $scope.tags
            .filter(x => !!x.rol)
            .map(x => x.rol);

        let words = $scope.tags
            .filter(x => !x.rol)
            .map(x => x.text);

        $state.go("jobs.search", {
            page: 1,
            filters: {
                roles,
                search: words.join(" ")
            }
        });
    };

    $scope.loadTags = function(query) {
        return $scope.availableRoles
            .filter((x) => {
                return x.name.toLowerCase()
                    .indexOf(query.toLowerCase()) !== -1;
            })
            .map((r) => {
                return {
                    rol: r,
                    text: r.name
                };
            });
    };

    $scope.updateJobs = function () {
        return jobsCollection.fetch(1, {
            params: {
                "page_size": 9 
            }
        })
        .then((jobs) => {
            
            
            var mdata = [];
            for(var i = 0; i< jobs._items.length; i++)
            {
                mdata.push(jobs._items[i].pk);
            }
            Apiv1Service.getInstance().post("jobs/userpostulationjobs", { pks: mdata })
                .then((response)=>{
                    var postulationjobs =  response.data.postulationjobs;
                    var usefavorite = response.data.usefavorite;
                    var hasfavoritejob = response.data.hasfavoritejob;
                    for(var i = 0; i< jobs._items.length; i++)
                    {
                        jobs._items[i].usefavorite = usefavorite;

                        var pk = jobs._items[i].pk;
                        if (postulationjobs.indexOf(pk) != -1)
                        {
                            jobs._items[i].postulated = true;
                        }
                        if (hasfavoritejob.indexOf(pk) != -1)
                        {
                            jobs._items[i].hasfavoritejob = true;
                        }
                        else
                        {
                            jobs._items[i].hasfavoritejob = false;
                        }
                    }
                    $scope.jobs = jobs;
                });
            
            
        });
    };

    $scope.updateCourses = function () {
        return coursesCollection.fetch(1, {
            params: {
                "page_size": 9 
            }
        })
            .then((courses) => {
                $scope.courses = courses;
            });
    };

    $scope.updateAreas = function () {
        return AreasService.list()
            .then((areas) => {
                $scope.areas = areas.slice(0, 10);
            });
    };

    $scope.updateRoles = function () {
        return RolesService.list()
            .then((roles) => {
                $scope.availableRoles = roles;
                $scope.roles = roles.splice(0, 10);
            });
    };

    $scope.updateLocations = function () {
        return GeoService.getCountries()
            .then((countries) => {
                $scope.locations = countries;
            });
    };

    $scope.updateCompanies = function () {
        return EmployerService.getCompanies()
            .then((companies) => {
                $scope.companies = companies;
            });
    };
    

    $q.all([
        $scope.updateJobs(),
        $scope.updateAreas(),
        $scope.updateRoles(),
        $scope.updateCourses(),
        $scope.updateLocations(),
        $scope.updateCompanies()
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$http",
    "JobsCollections",
    "CoursesCollections",
    "AreasService",
    "RolesService",
    "Apiv1Service",
    "GeoService",
    "EmployerService",
    factory
];
