"use strict";

/**
 * Geo module
 * @ngdoc module
 * @module  Geo
 */

const angular = require("angular");

require("ngmap");

const apiModule = require("../apiv1");

const geoService = require("./services/geo");
const pickerModal = require("./modals/picker");
const geoField = require("./directives/geofield");

module.exports = angular.module("RoleJob.Geo", [
    "ngMap",
    apiModule.name,
])
    .factory("GeoService", geoService) 
    .factory("GeoPickerModal", pickerModal)
    .directive("geoField", geoField)
;
