"use strict";

/**
 * Profile avatar image
 * @memberof Avatars
 * @ngdoc directive
 * @name profileAvatar
 */

const factory = function () {
    const AVATAR_URL = "/api/v1/avatars/profile";

    return {
        strict: "AE",
        replace: true,
        template: '<img ng-src="{{avatar.url}}" alt="">',
        scope: {
            "label": "@"
        },
        controller: [
            "$scope",
            "AvatarsService",
            ($scope, AvatarsService) => {
                $scope.label = $scope.label || "default";

                $scope.avatar = {
                    url: `${AVATAR_URL}/${$scope.label}`
                };

                var handler = AvatarsService.on("change_profile_avatar", () => {
                    var now = (new Date()).getTime();
                    $scope.avatar.url = `${AVATAR_URL}/${$scope.label}?${now}`;
                });

                $scope.$on("$destroy", () => {
                    handler();
                });

            }
        ]
    };

};

module.exports = factory;
