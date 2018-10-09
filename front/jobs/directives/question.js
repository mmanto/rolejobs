"use strict";

/**
 * Question item
 * @memberof Job
 * @ngdoc directive
 * @name questionItem
 */

const template = require("jobs/question_item.html");

const factory = function () {

    return {
        strict: "E",
        replace: true,
        template,
        scope: {
            question: "=",
            answer: "="
        }
    };

};

module.exports = factory;
