"use strict";

/**
 * Areas service
 * @memberof Jobs
 * @ngdoc service
 * @name JobsService
 */

const factory = function ($q, Apiv1Service) {

    const get = function (relpath, params = {}) {
        var path = `jobs/areas/${relpath}`;
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
     * List areas
     * @memberof JobsService 
     * @return {Promise}
     */
    const list = function () {
        return get(``);
    };

     /**
     * Get area data and subareas
     * @memberof JobsService
     * @param {number} id - The id of Area
     * @return {Promise}
     */
    const byId = function(id) {
        id = parseInt(id);
        return get(`${id}`);
    };

    /**
     * Get area data by slug
     * @memberof AreasService 
     * @param {string} slug 
     * @return {Promise}
     */
    const bySlug = function(slug) {
        return get(`${slug}`);
    };

    return {
        list,
        byId,
        bySlug,
    };

};

module.exports = [
    "$q",
    "Apiv1Service",
    factory
];
