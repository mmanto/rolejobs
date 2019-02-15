"use strict";

const employerMainTemplate = require("employer/dashboard.html");
const employerHomeTemplate = require("employer/home.html");
const employerJobsTemplate = require("employer/jobs.html");
const employerMessagesTemplate = require("employer/messages.html");
const employerJobDetailTemplate = require("jobs/job_detail_employer.html");
const employerJobPostulationTemplate = require("jobs/job_postulation_employer.html");
const employerCourseTemplate = require("employer/courses.html");
const employerCourseDetailTemplate = require("courses/course_detail_employer.html");
const employerCoursePostulationTemplate = require("courses/course_postulation_employer.html");


const resolveMe = ['EmployerService', (EmployerService) => {
    return EmployerService.getMe();
}];

module.exports = ["$stateProvider", ($stateProvider) => {

    $stateProvider
        .state("employer", {
            url: "/employer",
            abstract: true,
            template: `<div ui-view="employer-main">`
        })

        .state("employer.signup", {
            url: "/signup",
            views: {
                "employer-main": {
                    templateUrl: "/api/v1/employer/templates/signup.html",
                    controller: "EmployerSignupCtl"
                }
            }
        })

        .state("employer.main", {
            url: "/main",
            abstract: true,
            views: {
                "employer-main": {
                    template: employerMainTemplate,
                    controller: "EmployerCtl"
                }
            }
        })

            .state("employer.main.home", {
                url: "/home",
                views: {
                    "employer-main-main": {
                        template: employerHomeTemplate,
                        controller: 'EmployerHomeCtl'
                    }
                }
            })

            .state("employer.main.panel", {
                url: "/panel",
                views: {
                    "employer-main-main": { 
                        templateUrl: '/api/v1/employer/templates/employer.html',
                        controller: "EmployerPanelCtl"
                    }
                }
            })

            .state("employer.main.jobs", {
                url: "/jobs/{page:int}",
                params: {
                    page: null,
                    status: null,
                },
                views: {
                    "employer-main-main": { 
                        template: employerJobsTemplate,
                        controller: "EmployerJobsCtl"
                    }
                }
            })
            
            .state("employer.main.messages", {
                url: "/messages/",
                params: {
                    page: null,
                    status: null,
                },
                views: {
                    "employer-main-main": { 
                        template: employerMessagesTemplate,
                        controller: "EmployerMessagesCtl"
                    }
                }
            })

            .state("employer.main.jobedit", {
                url: "/job/:pk/edit",
                cache: false,
                params: {
                    pk: {
                        value: '-1',
                        squash: false, 
                    }
                },
                resolve: {
                    me: resolveMe, 
                },
                views: {
                    "employer-main-main": {
                        templateUrl: '/api/v1/jobs/templates/new_job.html',
                        controller: "NewJobCtl"  // jobs
                    }
                }
            })

            .state("employer.main.courses", {
                url: "/courses/{page:int}",
                params: {
                    page: null,
                    status: null,
                },
                views: {
                    "employer-main-main": { 
                        template: employerCourseTemplate,
                        controller: "EmployerCoursesCtl"
                    }
                }
            })

/* HC:Descomentar*/
            .state("employer.main.courseedit", {
                url: "/course/:pk/edit",
                params: {
                    pk: {
                        value: '-1',
                        squash: false, 
                    }
                },
                resolve: {
                    me: resolveMe, 
                },
                views: {
                    "employer-main-main": {
                        templateUrl: '/api/v1/courses/templates/new_course.html',
                        controller: "NewCourseCtl" 
                    }
                }
            })
            
            .state("employer.main.job", {
                url: "/job/{pk:int}/{page:int}",
                params: {
                    pk: {
                        squash: false, 
                    },
                    page: 1 
                },
                views: {
                    "employer-main-main": {
                        template: employerJobDetailTemplate,
                        controller: "EmployerJobDetailCtl"  // jobs
                    }
                }
            })

            .state("employer.main.jobpostulation", {
                url: "/job/{jobPk:int}/postulation/{pk:int}",
                params: {
                    jobPk: {
                        squash: false
                    },
                    pk: {
                        squash: false
                    }
                },
                views: {
                    "employer-main-main": {
                        template: employerJobPostulationTemplate,
                        controller: "EmployerJobPostulationCtl"
                    }
                }
            })
            
            .state("employer.main.course", {
                url: "/course/{pk:int}/{page:int}",
                params: {
                    pk: {
                        squash: false, 
                    },
                    page: 1 
                },
                views: {
                    "employer-main-main": {
                        template: employerCourseDetailTemplate,
                        controller: "EmployerCourseDetailCtl"  // course
                    }
                }
            })

            .state("employer.main.coursepostulation", {
                url: "/course/{coursePk:int}/postulation/{pk:int}",
                params: {
                    jobPk: {
                        squash: false
                    },
                    pk: {
                        squash: false
                    }
                },
                views: {
                    "employer-main-main": {
                        template: employerCoursePostulationTemplate,
                        controller: "EmployerCoursePostulationCtl"
                    }
                }
            })

    ;
}];
