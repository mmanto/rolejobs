"use strict";

/**
 * Confirm modal
 * @memberof Utils
 * @ngdoc directive
 * @name confirmModal
 */

const angular = require("angular");

const template = `
    <a class="close-reveal-modal" ng-click="$dismiss()">&#215;</a>
    <h3>{{title}}</h3>
    <p>{{ask}}</p>
    <div class="buttons">
    <a ng-click="accept()" class="rj-button">{{confirmLabel}}</a>
    <a ng-click="$dismiss()" class="rj-button alternative">{{cancelLabel}}</a>
    </div>
`;

const confirmModalFactory = function ($rootScope, $modal) {

    const confirmModalController = [
        "$scope",
        "$modalInstance",
        function ($scope, $modalInstance) {

            $scope.accept = function () {
                $modalInstance.close(true);
            }; 

        }
    ];        

    const open = function (msg, options = {}) {
        var scope;

        if (options.scope) {
            scope = options.scope;
            delete options.scope;
        } else {
            scope = $rootScope.$new(true);
        }

        angular.extend(scope, options, {
            confirmLabel: "Confirmar",
            cancelLabel: "Cancelar",
            title: "Confirme",
            ask: msg,
        });

        var modal = $modal.open({
            template: template,
            scope: scope,
            controller: confirmModalController,
            windowClass: 'confirm-modal alert-modal',
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
    confirmModalFactory
];
