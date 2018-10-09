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

const factory = function ($q, $scope, $state, JobsCollections, CoursesCollections,AreasService,
    RolesService) {

    const jobsCollection = JobsCollections.PublicJobs.getInstance();
    
    const coursesCollection = CoursesCollections.PublicCourses.getInstance();

    $scope.jobs = null; 
    $scope.areas = [];
    $scope.roles = [];
    $scope.availableRoles = [];

    $scope.courses = null; 

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
                $scope.jobs = jobs;
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

    $q.all([
        $scope.updateJobs(),
        $scope.updateAreas(),
        $scope.updateRoles(),
        $scope.updateCourses()
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "JobsCollections",
    "CoursesCollections",
    "AreasService",
    "RolesService",
    factory
];
