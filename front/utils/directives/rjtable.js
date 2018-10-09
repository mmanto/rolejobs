"use strict";

/**
 * RJ's style table
 * @memberof Utils
 * @ngdoc directive
 * @name rjTable
 */

const rjTableFactory = function () {

    return {
        strict: "AE",
        link (scope, element) {
            element
                .addClass("rj-table");
        }
    };

};

module.exports = rjTableFactory;
