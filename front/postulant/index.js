"use strict";

/**
 * @module Rolejob.postulant 
 */

const angular = require("angular");

const routes = require("./routes");
const postulantController = require("./controllers/postulant");
const homeController = require("./controllers/home");
const postulantCvController = require("./controllers/cv");
const postulationsController = require("./controllers/postulations");
const messagesController = require("./controllers/messages");
const favoritesController = require("./controllers/favorites");
const postulantService = require("./services/postulant");
const postulationsService = require("./services/postulantspostulations");
const messagesService = require("./services/postulantsmessages");
const favoritesService = require("./services/postulantsfavorites");
const coursesService = require("./services/postulantscourses");
const postulantNewPEModalService = require("./modals/newpe");
const postulantNewEducationModalFactory = require("./modals/neweducation");
const postulantNewReferenceModalFactory = require("./modals/newreference");
const postulantNewLanguageModalFactory = require("./modals/newlanguage");
const postulantNewComputerknowledgeModalFactory = require("./modals/newcomputerknowledge");
const postulantNewAdditionalknowledgeModalFactory = require("./modals/newadditionalknowledge");
const postulantNewWorkpreferenceModalFactory = require("./modals/newworkpreference");
const newCertificationModalFactory = require("./modals/newcert");
const postulationModal = require("./modals/postulation");
const messageModal = require("./modals/message");
const postulationItem = require("./directives/postulation");
const experienceItem = require("./directives/experience");
const educationItem = require("./directives/education");
const completedProfileDirective = require("./directives/completedprofile");
const favoriteItem = require("./directives/favorite");

module.exports = angular.module("RoleJob.postulant", [

])
    .config(routes)
    .controller("PostulantCtl", postulantController)
    .controller("PostulantHomeCtl", homeController)
    .controller("PostulantCvCtl", postulantCvController)
    .controller("PostulatPostulationsCtl", postulationsController)
    .controller("PostulatMessagesCtl", messagesController)
    .controller("PostulatFavoritesCtl", favoritesController)
    .factory("PostulantService", postulantService)
    .factory("PostulantPostulationsService", postulationsService)
    .factory("PostulantMessagesService", messagesService)
    .factory("PostulantFavoritesService", favoritesService)
    .factory("PostulantCoursesService", coursesService)     
    .factory("PostulantNewPEModal", postulantNewPEModalService)
    .factory("PostulantNewEducationModal", postulantNewEducationModalFactory)
    .factory("PostulantNewReferenceModal", postulantNewReferenceModalFactory)
    .factory("PostulantNewLanguageModal", postulantNewLanguageModalFactory)
    .factory("PostulantNewComputerknowledgeModal", postulantNewComputerknowledgeModalFactory)
    .factory("PostulantNewAdditionalknowledgeModal", postulantNewAdditionalknowledgeModalFactory)
    .factory("PostulantNewWorkpreferenceModal", postulantNewWorkpreferenceModalFactory)
    .factory("PostulantNewCertificationModal", newCertificationModalFactory)
    .factory("PostulantPostulationModal", postulationModal)
    .factory("PostulantMessageModal", messageModal)
    .directive("postulantPostulationItem", postulationItem)
    .directive("experienceItem", experienceItem)
    .directive("educationItem", educationItem)
    .directive("postulantCompletedProfile", completedProfileDirective)
    .directive("postulantFavoriteItem", favoriteItem)
;
