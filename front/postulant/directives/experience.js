"use strict";

/**
 * Experience directive
 * @memberof Postulant
 * @ngdoc directive
 * @name experienceItem
 */

const template = require("postulant/experience_item.html");

const contactsTemplate = `
<a class="close-reveal-modal" ng-click="$dismiss()">&#215;</a>
<div 
  ng-if="references.length"
  rj-table-collection
  collection-schema="contactsSchema"
  collection-data="references"
  class="compact"
></div>
`;

const factory = function () {

    return {
        strict: "E",
        repalce: true,
        template,
        scope: {
            experience: "="
        },
        controller: ["$scope", "$modal", ($scope, $modal) => {
            
            $scope.viewReferences = function () {

                var $modalScope = $scope.$new(true);
                $modalScope.references = $scope.experience.references;
                $modalScope.contactsSchema = {
                    $id: "id",
                    "type_text": "Tipo",
                    name: "Nombre",
                    phone: "Teléfono",
                    email: "Email"
                };

                $modal.open({
                    template: contactsTemplate,
                    windowClass: "rj-modal",
                    scope: $modalScope
                });
            };

        }]
    };

};

module.exports = factory;
