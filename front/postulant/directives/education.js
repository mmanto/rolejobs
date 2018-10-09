"use strict"; 

/**
 * Education item for postulant
 * @memberof Postulant
 * @ngdoc directive
 * @name educationItem
 */

const educationTemplate = require("postulant/education_item.html");

const factory = function () {
    return {
        strict: "E",
        replace: true,
        template: educationTemplate,
        scope: {
            education: "="
        }
    };
};

module.exports = factory;
