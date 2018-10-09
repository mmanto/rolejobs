"use strict";

const angular = require("angular");

const apiv1Service = require("./services/apiv1");
const recordSetService = require("./services/recordset");
const collectionService = require("./services/collection");

module.exports = angular.module("RoleJobs.apiv1", [
])
    .factory("Apiv1Service", apiv1Service)
    .factory("RecordSet", recordSetService)
    .factory("CollectionService", collectionService)
;
