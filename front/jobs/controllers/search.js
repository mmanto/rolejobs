"use strict";

/**
 * Job search controller
 * @memberof Jobs
 * @ngdoc controller
 * @name JobSearchCtl
 */

const angular = require("angular");

const factory = function ($q, $scope, $state, $params, JobsCollections,
                                                              FiltersService) {

    const FILTER_SEARCH = "filter_search";

    const jobs = JobsCollections.PublicJobs.getInstance(); 

    $scope.jobs = [];

    $scope.jobsInfo = {
        results: 0
    };

    $scope.searchQuery = "";

    $scope.filters = [ 
        {
            id: "roles",
            name: "Roles",
            type: "list",
            multi: true,
            value: [],
            choices: [],
        },{
            id: "title_role",
            name: "Título",
            type: "list",
            multi: false,
            value: null,
            choices: [],
        },{
            id: "position",
            name: "Posición",
            type: "list",
            multi: false,
            value: null,
            choices: [],
        },{
            id: "hierarchy",
            name: "Jerarquía",
            type: "list",
            multi: false,
            value: null,
            choices: []
        },{
            id: "job_type",
            name: "Tipo",
            type: "list",
            multi: false,
            value: null,
            choices: []
        },
        {
            id: "country",
            name: "País",
            type: "list",
            multi: false,
            value: null,
            choices: []
        }
    ];

    const getFilter = function(id) {
        return $scope.filters
            .find(x => x.id === id);
    };

    const getFiltersValues = function () {
        $scope.filters.reduce((result, filter) => {
            result[filter.id] = filter.value;
        }, {});
    };

    $scope.actualPage = $params.page || 1;

    $scope.updateFilters = function () {
        console.log($scope.filters);
        return $scope.updateJobs();
    };

    $scope.removeFilter = function(filter, value = null) {

        if (filter && filter.multi && value) {
            filter.value = filter.value.filter((i) => {
                return i !== value;
            });
        } else if (filter) {
            filter.value = filter.multi ? [] : null;
        }

        return $scope.updateFilters();    
    };

    $scope.changePage = function (pag) {
        return $state.go($state.$current, {
            page: pag,
            filters: getFiltersValues() 
        });
    };

    const flatValue = function (val) {
        if (typeof val === "object") {
            return val.pk || val.value || null;
        } else {
            return val;
        }
    };

    $scope.clearFilters = function () {
        $scope.filters.forEach((filter) => {
            filter.value = filter.multi ? [] : null;
        });

        return $scope.updateJobs();
    };

    $scope.updateJobs = function () {

        var params = $scope.filters
            .filter((filter) => {
                return filter.multi ? filter.value.length : !!filter.value;
            })
            .map((filter) => {
                let value;

                if (filter.multi) {
                    value = filter.value.map(flatValue).join(",");
                } else {
                    value = flatValue(filter.value);
                }

                return {
                    id: filter.id,
                    value
                };

            })
            .reduce((parms, filter) => {
                parms[`filter_${filter.id}`] = filter.value;
                return parms;
            }, {});

        if ($scope.searchQuery.trim() !== "") {
            params[FILTER_SEARCH] = $scope.searchQuery;
        }

        return jobs.fetch($scope.actualPage, {params})
            .then((jobs) => {
                $scope.jobsInfo.results = jobs.totalLength;
                $scope.jobs = jobs;
            })
            .catch((err) => {
                if (err.status === 404) {
                    return $scope.changePage(1);
                }
            });
    
    };

    $scope.updateFiltersChoices = function () {

        return FiltersService.getJobsChoices()
            .then((filters) => {
                angular.forEach(filters, (choices, fid) => {

                    var filter = getFilter(fid);

                    if (!filter) {
                        console.log(`No ${fid} on filters`);
                        return;
                    }

                    filter.choices = choices.map((c) => {
                        if (typeof c.pk === "undefined") {
                            c.pk = c.key || c.id;
                        }

                        return c;
                    });

                });
            });
    };

    $scope.$watch("searchQuery", () => {
        return $scope.updateJobs();    
    });

    // Add values for filters:
    
    if ($params.filters) {
        for (let fname in $params.filters) {

            if (!fname.match(/^[a-z]/i)) {
                continue;
            }

            if (fname === "search") {
                $scope.searchQuery = $params.filters[fname];
                continue;
            }

            let filter = getFilter(fname);

            if (!filter) {
                console.log(`Filter ${fname} unknow`);
                continue;
            }

            filter.value = $params.filters[fname];

        }
    }

    return $q.all([
        $scope.updateJobs(),
        $scope.updateFiltersChoices(),
    ]);

};

module.exports = [
    "$q",
    "$scope",
    "$state",
    "$stateParams",
    "JobsCollections",
    "FilterChoicesService",
    factory
];
