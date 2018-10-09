"use strict";

/**
 * Employer module
 * @module Employer
 */

const angular = require("angular");

const routes = require("./routes");
const employerService = require("./services/employer");
const employerCtl = require("./controllers/employer");
const signupController = require("./controllers/signup");
const employerJobsController = require("./controllers/jobs");
const employerMessagesController = require("./controllers/messages");
const employerCoursesController = require("./controllers/courses");
const employerPanelController = require("./controllers/panel");
const jobDetailController = require("./controllers/job");
const courseDetailController = require("./controllers/course");
const jobPostulationController = require("./controllers/jobpostulation");
const postulantItem = require("./directives/postulant");

module.exports = angular.module("RoleJob.Employer", [
])
    .factory("EmployerService", employerService)
    .controller("EmployerCtl", employerCtl)
    .controller("EmployerSignupCtl", signupController)
    .controller("EmployerJobsCtl", employerJobsController)
    .controller("EmployerMessagesCtl", employerMessagesController)
    .controller("EmployerCoursesCtl", employerCoursesController)
    .controller("EmployerPanelCtl", employerPanelController)
    .controller("EmployerJobDetailCtl", jobDetailController)
    .controller("EmployerCourseDetailCtl", courseDetailController)
    .controller("EmployerJobPostulationCtl", jobPostulationController)
    .directive("jobPostulantItem", postulantItem)
    .config(routes)
;
