"use strict";

/**
 * Colection of util filters, directives, etc.
 * @module Utils 
 */

const angular = require("angular");

const extendibleBuiltinFactory = require("./services/extendiblebuiltin");
const formHelperFactory = require("./services/formhelper");
const alertModalFactory = require("./modals/alert");
const apiErrorsAlertModalFactory = require("./modals/apierrorsalert");
const confirmModalFactory = require("./modals/confirm");
const stateTabDirective = require("./directives/statetab");
const datetimepickerFactory = require("./directives/datetimepicker");
const rjTableFieldFactory = require("./directives/rjtablefield");
const rjTableFactory = require("./directives/rjtable");
const rjTableCollectionFactory = require("./directives/rjtablecollection");
const rjIconFactory = require("./directives/rjicon");

module.exports = angular.module("RoleJob.Utils", [
])
    .factory("extendibleBuiltin", extendibleBuiltinFactory)
    .factory("FormHelper", formHelperFactory)
    .factory("AlertModal", alertModalFactory)
    .factory("ConfirmModal", confirmModalFactory)
    .factory("ApiErrorsAlertModal", apiErrorsAlertModalFactory)
    .directive("stateTab", stateTabDirective)
    .directive("datetimepicker", datetimepickerFactory)
    .directive("rjTableField", rjTableFieldFactory)
    .directive("rjTable", rjTableFactory)
    .directive("rjTableCollection", rjTableCollectionFactory)
    .directive("rjIcon", rjIconFactory)
;
