"use strict";

const courseTemplate = require("courses/course.html");

/**
 * Course directive, the jcourse  item
 * @memberof Courses
 * @ngdoc directive
 * @name courseItem
 */

const courseItem = function () {

    return {
        strict: "E",
        replace: true,
        template: courseTemplate,
        scope: {
            course:"="
        }
    };

};

module.exports = courseItem;
