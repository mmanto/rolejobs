"use strict";

/**
 * Choices for fitlers
 * @memberof Filters
 * @ngdoc service
 * @name FilterChoicesService
 */ 

const factory = function (Apiv1Service) {

    const get = function (path, params = {}) {

        return Apiv1Service.getInstance().get(path, params) 
            .then((result) => {
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Invalid response");
                }
            });
    };

    const getJobsChoices = function () {
        return get("jobs/as_choices");
    };

    return {
        getJobsChoices,
    };

};

module.exports = [
    "Apiv1Service",
    factory
];
