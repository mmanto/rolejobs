"use strict";

/**
 * Crop image modal
 * @memberof Cropper
 * @ngdoc service
 * @name CroppterModal
 */

const template = require("cropper/modal.html");

const factory = function ($modal) {

    const modalCtl = [
        "$scope",
        "options",
    function ($scope, options) {

        options.width = options.width || 150;
        options.height = options.height || 150;

        $scope.image = {
            src: options.src || null
        };

        $scope.width = options.width;
        $scope.height = options.height;

        $scope.sizes = {
            "width": `${options.width}px`,
            "height":`${options.height}px`
        };

        $scope.save = function () {
            $scope.$close($scope.image);
        };
        $scope.cancel = function () {
            $scope.$dismiss('canceled');
        };

    }];

    const open = function (options = {}) {

        var modal = $modal.open({
            template: template,
            backdrop: 'static',
            keyboard: false,
            windowClass: 'cropper-modal',
            controller: modalCtl,
            resolve: {
                options() {
                    return options;
                }
            }
        });

        return modal;

    };    

    return {
        open    
    };

};

module.exports = [
    "$modal",
    factory
];
