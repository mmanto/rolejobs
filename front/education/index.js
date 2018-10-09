"use strict";

/**
 * @module Education 
 */

const angular = require("angular");

const educationServiceFactory = require("./services/education");

module.exports = angular.module("RoleJob.Education", [

])
    .factory("EducationService", educationServiceFactory)
;
