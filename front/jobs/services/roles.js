"use strict";

/**
 * Roles service
 * @memberof Jobs
 * @ngdoc service
 * @name RolesService
 */

const factory = function ($q, Apiv1Service) {

    const get = function (relpath, params = {}) {
        var path = `jobs/roles/${relpath}`;
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
     * List roles
     * @memberof RolesService 
     * @return {Promise}
     */
    const list = function () {
        return get(``);
    };

    return {
        list,
    };

};

module.exports = [
    "$q",
    "Apiv1Service",
    factory
];
