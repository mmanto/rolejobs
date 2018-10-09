"use strict";

/**
 * Filters app, for filter management 
 * @module Filters
 */

const angular = require("angular");

const choicesService = require("./services/choices");
const filterDirective = require("./directives/filter");

module.exports = angular.module("RoleJob.Filters", [
])
    .factory("FilterChoicesService", choicesService)
    .directive("rjFilter", filterDirective)
;
