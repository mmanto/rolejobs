"use strict";

/**
 * Postulation modal for postulant
 * @memberof Postulant
 * @ngdoc service
 * @name PostulantPostulationModal
 */

const factory = function ($modal) {

    const template = require("postulant/postulation_modal.html");

    const modalCtl = [
        "$scope",
        "postulation",
    function ($scope, postulation) {
        $scope.postulation = postulation;
    }];

    const open = function (data) {

        if (!data) {
            throw new Error("Data can't be null");
        }

        var modal = $modal.open({
            template: template,
            controller: modalCtl,
            windowClass: 'postulation-modal',
            resolve: {
                postulation() {
                    return data;
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
