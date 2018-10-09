"use strict";

/**
 * Confirm modal
 * @memberof Utils
 * @ngdoc directive
 * @name AlertModal
 */

const angular = require("angular");

const template = `
    <a class="close-reveal-modal" ng-click="$dismiss()">&#215;</a>
    <h3>{{title}}</h3>
    <p>{{msg}}</p>
    <div class="buttons">
        <a ng-click="accept()" class="rj-button">
            {{acceptLabel}}
        </a>
    </div>
`;

const factory = function ($rootScope, $modal) {

    const modalController = [
        "$scope",
        "$modalInstance",
        function ($scope, $modalInstance) {

            $scope.accept = function () {
                $modalInstance.close(true);
            }; 

        }
    ];        

    const open = function (msg, title = "Attención", options = {}) {
        var scope;

        if (options.scope) {
            scope = options.scope;
            delete options.scope;
        } else {
            scope = $rootScope.$new(true);
        }

        angular.extend(scope, options, {
            acceptLabel: "Aceptar",
            title: title,
            msg: msg,
        });

        var modal = $modal.open({
            template: template,
            scope: scope,
            controller: modalController,
            windowClass: 'alert-modal',
            backdrop: true
        });

        return modal.result;

    };

    return {
        open
    };

};

module.exports = [
    "$rootScope",
    "$modal",
    factory
];
