"use strict";

const jobsByAreaTemplate = require("jobs/jobs_by_area.html");
const jobsByRolesTemplate = require("jobs/jobs_by_roles.html");
const jobDetailTemplate = require("jobs/job_detail.html");
const jobPostulationTemplate = require("jobs/job_postulate_front.html");
const jobSearchTemplate = require("jobs/jobs_search.html");

module.exports = ["$stateProvider", ($stateProvider) => {

    $stateProvider
        .state("jobs", {
            url: "/jobs",
            abstract: true,
            template: `<div class="jobs-screen" ui-view>`,
            controller: "JobsCtl" 
        })

        .state("jobs.detail", {
            url: "/detail/{id:int}",
            params: {
                id: {
                    squash: false
                }
            },
            resolve: {
                jobData: [
                    "$stateParams",
                    'JobsCollections'
                    ,($stateParams, JobsCollections) => {
                        return JobsCollections.PublicJobs.getInstance().getItem($stateParams.id);
                    }
                ]
            },
            controller: "JobDetailCtl",
            template: jobDetailTemplate
        })

        .state("jobs.postulate", {
            url: "/postulate/{id:int}",
            params: {
                id: {
                    squash: false
                }
            },
            resolve: {
                jobData: [
                    "$stateParams",
                    "JobsCollections",
                    ($stateParams, JobsCollections) => {
                        return JobsCollections.PublicJobs
                            .getInstance()
                            .getItem($stateParams.id);
                    }
                ]
            },
            template: jobPostulationTemplate,
            controller: "JobPostulateCtl"
        })

        .state("jobs.byArea", {
            url: "/area/:area/{page:int}",
            params: {
                area: {
                    squash: false 
                },
                page: null,
                filters: null,
                toSubarea: null,
            },
            resolve: {
                area: [
                    "$stateParams",
                    "AreasService",
                    ($stateParams, AreasService) => {
                        return AreasService.bySlug($stateParams.area);
                    }
                ] 
            },
            controller: "JobsByAreaCtl",
            template: jobsByAreaTemplate
        })

        .state("jobs.byRoles", {
            url: "/roles/{page:int}",
            params: {
                page: null,
                filters: null,
            },
            controller: "JobsByRolesCtl",
            template: jobsByRolesTemplate
        })

        .state("jobs.search", {
            url: "/search/{page:int}",
            params: {
                page: null,
                filters: null,
            },
            controller: "JobSearchCtl",
            template: jobSearchTemplate
        })


    ;
}];
