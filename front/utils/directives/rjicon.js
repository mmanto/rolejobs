"use strict";

/**
 * Icons rj-style
 * @memberof Utils
 * @ngdoc directive
 * @name rjIcon
 */

const template = `<i class="rj-icon"><img ng-src="{{iconSrc}}"></i>`;

const factory = function () {

    return {
        strict: "E",
        replace: true,
        template,
        scope: {
            icon: "@"
        },
        link (scope) {
            const path = `/static/img/icons/${scope.icon}.png`;
            scope.iconSrc = path;
        }
    };

};

module.exports = factory;
