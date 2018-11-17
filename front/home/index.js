"use strict";

require('./tooltip');
require('./company-carousel');

const angular = require('angular');

const statsDataDirective = require("./directives/stats");

const homeController = require("./controllers/home");
const contactController = require("./controllers/contact");

module.exports = angular.module('RoleJobs.home', [
    'ngTagsInput'
])
    .directive('statsData', statsDataDirective)
    .controller("HomeCtl", homeController)
    .controller("ContactCtl", contactController)
;
