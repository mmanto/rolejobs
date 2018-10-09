"use strict";

/**
 * @module Courses 
 */

const angular = require("angular");

const routes = require("./routes");

const courseItemDirective = require("./directives/course");
const coursesService = require("./services/courses");
const coursesCollectionsService = require("./services/collections");
const postulationsService = require("./services/postulations");
const newCourseController = require("./controllers/newcourse");
const coursesController = require("./controllers/courses");
const detailController = require("./controllers/detail");
const postulateController = require("./controllers/postulate");

module.exports = angular.module("RoleJob.Courses", [

])
    .config(routes)
    .directive("courseItem", courseItemDirective)
    .factory("CoursesService", coursesService)    
    .factory("CoursesCollections", coursesCollectionsService)
    .factory("PostulationsService", postulationsService)
    .controller("NewCourseCtl", newCourseController)
    .controller("CoursesCtl", coursesController)
    .controller("CourseDetailCtl", detailController)
    .controller("CoursePostulateCtl", postulateController)
;
