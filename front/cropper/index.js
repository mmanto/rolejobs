"use strict";

/**
 * Cropper module, to manipulate images
 * @module Cropper
 */

const angular = require("angular");
require("cropit");

const imageCropper = require("./directives/imagecropper");
const croppterModal = require("./modals/croppter");

module.exports = angular.module("Cropper",[])
    .directive("imageCropper", imageCropper)
    .factory("CroppterModal", croppterModal)
;
