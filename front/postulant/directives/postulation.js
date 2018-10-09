"use strict";


/**
 * Postulation directive (for postulant)
 * @memberof Postulant
 * @ngdoc directive
 * @name postulantPostulationItem
 */

const factory = function () {
    const postulationTemplate = require("postulant/postulation_item.html");

    return {
        strict: "E",
        replace: true,
        template: postulationTemplate,
        scope: {
            "postulation": "=",
            "viewCb": "="
        }
    };

};

module.exports = factory;
