"use strict";

/**
 * @module Jobs 
 */

const angular = require("angular");

const routes = require("./routes");

const jobItemDirective = require("./directives/job");
const selectRoles = require("./directives/selectroles");
const questionItem = require("./directives/question");
const jobsService = require("./services/jobs");
const jobsCollectionsService = require("./services/collections");
const areasService = require("./services/areas");
const techsService = require("./services/techs");
const rolesService = require("./services/roles");
const postulationsService = require("./services/postulations");
const techModal = require("./modals/ittech");
const questionModal = require("./modals/question");
const newJobController = require("./controllers/newjob");
const jobsController = require("./controllers/jobs");
const byAreaController = require("./controllers/byarea");
const byRolesController = require("./controllers/byroles");
const detailController = require("./controllers/detail");
const postulateController = require("./controllers/postulate");
const jobSearchsController = require("./controllers/search");

module.exports = angular.module("RoleJob.Jobs", [

])
    .config(routes)
    .directive("jobItem", jobItemDirective)
    .directive("selectRoles", selectRoles)
    .directive("questionItem", questionItem)
    .factory("JobsService", jobsService)   
    .factory("JobsCollections", jobsCollectionsService)
    .factory("AreasService", areasService)
    .factory("TechsService", techsService)
    .factory("RolesService", rolesService)
    .factory("PostulationsService", postulationsService)
    .factory("ITTechModal", techModal)
    .factory("QuestionModal", questionModal)
    .controller("NewJobCtl", newJobController)
    .controller("JobsCtl", jobsController)
    .controller("JobsByAreaCtl", byAreaController)
    .controller("JobsByRolesCtl", byRolesController)
    .controller("JobDetailCtl", detailController)
    .controller("JobPostulateCtl", postulateController)
    .controller("JobSearchCtl", jobSearchsController)
;
