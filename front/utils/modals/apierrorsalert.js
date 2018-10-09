"use strict";

/**
 * Confirm modal
 * @memberof Utils
 * @ngdoc directive
 * @name ApiErrorsAlertModal
 */

const angular = require("angular");

const template = `
    <a class="close-reveal-modal" ng-click="$dismiss()">&#215;</a>
    <h3>{{title}}</h3>
    <p>{{msg}}</p>
    <div ng-repeat="field in errors track by field.field">
      <h5>{{ field.field }}</h5>
      <ul class="errors">
        <li ng-repeat="err in field.msgs">
          {{ err }}
        </li>
      <ul>
    </div>
    <div class="buttons">
        <a ng-click="accept()" class="rj-button">
            {{acceptLabel}}
        </a>
    </div>
`;

const DEFAULT_TITLE = "Error al enviar";
const DEFAULT_MSG = "Su formulario contiene algunos errores, verifiquelos" + 
                    " y reintente.";

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

    const open = function (errors, namesTable = {}, msg = DEFAULT_MSG,
                                    title = DEFAULT_TITLE, options = {}) {
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
            errors: errors
        });

        scope.errors = scope.errors.map((e) => {
            var fieldName = namesTable[e.field] || e.field;
            return {
                field: fieldName,
                msgs: e.msgs
            };
        });

        var modal = $modal.open({
            template: template,
            scope: scope,
            controller: modalController,
            windowClass: 'api-errors-modal',
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
