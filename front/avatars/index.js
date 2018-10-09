"use strict";

/**
 * @module Avatars
 */

const angular = require("angular");

const avatarsService = require("./services/avatars");
const profileAvatarFactory = require("./directives/avatar");

module.exports = angular.module("RoleJob.Avatars", [

])
    .factory("AvatarsService", avatarsService)
    .directive("profileAvatar", profileAvatarFactory)
;
