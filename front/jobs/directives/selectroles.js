"use strict";

/**
 * RJ's style table Collection 
 * @memberof Jobs
 * @ngdoc directive
 * @name selectRoles
 */

const angular = require('angular');

const factory = function() {

    const template = `
        <ul class="select-roles">
        <li
            ng-repeat="role in roles.items track by role.pk"
            class="role"
        >
          <input
            type="checkbox"
            ng-model="roles.selected[role.pk]"
            name="role_check_{{ role.pk }}"
            id="{{ uuid }}_role_check_{{ role.pk }}"
          >
            <label
              for="{{ uuid }}_role_check_{{ role.pk }}"
              ng-bind="role.name"
            ></label>
        </li>
        </ul>
    `;

    return {
        strict: "EA",
        replace: true,
        template: template,
        require: '?ngModel', 
        scope: {
            onChange: "&"
        },
        link (scope, el, attrs, ngModel) {

            const clearPks = function () {
                var pks = [];
               
                angular.forEach(scope.roles.selected, (v, k) => {
                    if (v) {
                        pks.push(parseInt(k));
                    }
                });

                scope.onChange({
                    $items: pks
                });

                return pks;

            };

            const setValue = function (value) {
                scope.roles.selected = {};

                angular.forEach(value, (pk) => {
                    scope.roles.selected[`${pk}`] = true;
                });
           
            };

            if (ngModel) {
                ngModel.$setViewValue(ngModel.$modelValue);
                setValue(ngModel.$modelValue);
                
                ngModel.$render = function () {
                    setValue(ngModel.$viewValue);
                };

            }

            var handler = scope.$watchCollection('roles.selected', () => {
                if (ngModel) {
                    ngModel.$setViewValue(clearPks());
                }
            });

            scope.$on('$destroy', handler);

        },
        controller: [
            '$scope',
            'RolesService',
            ($scope, RolesService) => {

                $scope.uuid = (new Date()).getTime().toString(36);
                $scope.roles = {
                    items: [],
                    selected: {}
                };

                RolesService.list().then((roles) => {
                    $scope.roles.items = roles;
                }); 
            }
        ]
    };
};

module.exports = factory;
