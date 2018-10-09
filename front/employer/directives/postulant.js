"use strict";

/**
 * Postulat directive (for employers)
 * @memberof Employer 
 * @ngdoc directive
 * @name jobPostulantItem
 */

const factory = function () {
    const postulationTemplate = require("employer/postulant_item.html");

    return {
        strict: "E",
        replace: true,
        template: postulationTemplate,
        scope: {
            "postulation": "=",
            "viewPostulation": "="
        }
    };

};

module.exports = factory;
