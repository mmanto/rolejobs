"use strict";


/**
 * Postulation directive (for postulant)
 * @memberof Postulant
 * @ngdoc directive
 * @name postulantMessageItem
 */

const factory = function () {
    const messageTemplate = require("postulant/message_item.html");

    return {
        strict: "E",
        replace: true,
        template: messageTemplate,
        scope: {
            "postulation": "=",
            "viewCb": "="
        }
    };

};

module.exports = factory;
