"use strict";

/**
 * Employer service
 * @memberof Employer
 * @ngdoc service
 * @name EmployerService
 * @param {service} $q
 * @param {service} Apiv1Service
 */

const EmployerService = function ($q, Apiv1Service) {

    const get = function(subpath, params={}) {
        const api = Apiv1Service.getInstance();

        return api.get(`employer/${subpath}`, params)
            .then((result) => {
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Inválida response data");
                }
            });
   
    };

    const post = function (subpath, data = {}, params = {}) {
        const api = Apiv1Service.getInstance();
        data = Apiv1Service.normalize(data);

        return api.post(`employer/${subpath}`, data, params)
            .then((result) => {
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Inválida response data");
                }
            });

    };

    const put = function (subpath, data = {}, params = {}) {
        const api = Apiv1Service.getInstance();
        data = Apiv1Service.normalize(data);

        return api.put(`employer/${subpath}`, data, params)
            .then((result) => {
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Inválida response data");
                }
            });

    };


    /**
     * Get employer data
     * @memberof EmployerService
     * @return {Promise}
     */
    const getMe = function () {
        return get("employer");
    };

    const saveMe = function (data) {
        return put("employer", data);
    };

    /**
     * Signup new employer
     * @memberof EmployerService
     * @param {object} data - Form data 
     * @return {Promise:Null|Object} Promise
     */
    const signup = function (data) {
        return post('signup', data);
    };


    const getCompanies = function() {
        const api = Apiv1Service.getInstance();

        return api.get(`employer/companies`)
            .then((result) => {
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Inválida response data");
                }
            });
   
    };

    const getGlobalStats = function() {
        const api = Apiv1Service.getInstance();

        return api.get(`employer/globalstats`)
            .then((result) => {
                if (result.data) {
                    return result.data;
                } else {
                    throw new Error("Inválida response data");
                }
            });
   
    };

    return {
        getMe,
        saveMe,
        signup,
        getCompanies,
        getGlobalStats
    };

    

};

module.exports = [
    "$q",
    "Apiv1Service",
    EmployerService
];
