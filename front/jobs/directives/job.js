"use strict";

const jobTemplate = require("jobs/job.html");

/**
 * Job directive, the job item
 * @memberof Jobs
 * @ngdoc directive
 * @name jobItem
 */

const jobItem = function () {

    return {
        strict: "E",
        replace: true,
        template: jobTemplate,
        scope: {
            job:"="
        }
    };

};

module.exports = jobItem;
