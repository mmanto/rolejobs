"use strict";


/**
 * Postulation directive (for postulant)
 * @memberof Postulant
 * @ngdoc directive
 * @name postulantFavoriteItem
 */

const factory = function () {
    const favoriteTemplate = require("postulant/favorite_item.html");

    return {
        strict: "E",
        replace: true,
        template: favoriteTemplate,
        scope: {
            "favorite": "=",
            "viewCb": "="
        }
    };

};

module.exports = factory;
