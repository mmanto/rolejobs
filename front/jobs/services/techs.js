"use strict";

/**
 * Techs service
 * @memberof Jobs
 * @ngdoc service
 * @name TechsService
 */

const factory = function ($q, Apiv1Service) {

    const get = function (relpath, params = {}) {
        var path = `jobs/technologies/${relpath}`;
        return Apiv1Service.getInstance().get(path, params) 
            .then((result) => {
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Invalid response");
                }
            });
    };

    /**
     * List technologies
     * @memberof TechsService 
     * @return {Promise}
     */
    const list = function () {
        return get(``);
    };

     /**
     * Get tech data and subtechnologies
     * @memberof TechsService
     * @param {number} id - The id of Technology 
     * @return {Promise}
     */
    const byId = function(id) {
        id = parseInt(id);
        return get(`${id}`);
    };

    return {
        list,
        byId,
    };

};

module.exports = [
    "$q",
    "Apiv1Service",
    factory
];
