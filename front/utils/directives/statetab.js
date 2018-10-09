"use strict";

/**
 * State tab, for tabs + states
 * @ngdoc directive
 * @name stateTab
 * @memberof Utils
 */

const template = `
<li class="tab-title" role="presentation" ng-class="{active: active}">
    <a ui-sref="{{uiSref}}" role="tab" tabindex="0" aria-selected="{{active}}">
        {{ label | translate }}
    </a>
</li>`;

const stateTab = function () {

    return {
        strict: "EA",
        replace: true,
        template,
        scope: {
            uiSref: "@",
            label: "@"
        },
        controller: [
            "$scope",
            "$state",
            ($scope, $state) => {

                $scope.update = function () {
                    var srefInfo = $state.get($scope.uiSref);

                    $scope.active = false;

                    if (srefInfo && srefInfo.name === $state.current.name) {
                        $scope.active = true;
                    } else {
                        $scope.active = false;
                    }
                    
                    // Nullify
                    srefInfo = null;
                    srefInfo = undefined;

                };

                var stateChangeHandler = $scope.$on(
                    "$stateChangeSuccess", () => {
                        $scope.update();
                    }
                );

                $scope.$on("$destroy", stateChangeHandler);

                $scope.update();
                
            }
        ] 
    };

};

module.exports = stateTab;
