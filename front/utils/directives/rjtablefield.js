"use strict";

/**
 * Tables rj's style
 * @memberof Utils
 * @name rjTableField
 * @ngdoc directive 
 */

const rjTableFieldFactory = function () {

    return {
        restrict: "AE",
        link(scope, element, attrs) {
            element.addClass("rj-table-field");

            if (attrs.align && attrs.align !== "") {
                element.addClass(`text-${attrs.align}`);
            }
        } 
    };

};

module.exports = rjTableFieldFactory;
