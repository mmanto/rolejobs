"use strict";

const _ = require("underscore");

module.exports = [
    "$q",
    "$http",
/**
 * @memberof apiv1 
 * @ngdoc service 
 * @name ApiV1 
 * @param {service} $q
 * @param {service} $http 
 * @description
 *      Apiv1 connector service 
 */
function ($q, $http) {

    const API_URL = "/api/v1";

    var instance;

    const toUndorescore = function (text) {
        return text.replace(
                /(?:^|\.?)([A-Z])/g,
                (x,y) => `_${y.toLowerCase()}`
                ).replace(/^_/, "");
    };

    /**
     * ApiV1 class
     * @memberof apiv1
     */

    class ApiV1 {

        /**
         * Do a request 
         * @param {String} method - This can be "GET", "POST", "PUT" or "DELETE"
         * @param {String} path - The path 
         * @param {Object} [data] - If is a POST o PUT, the data to send
         * @param {Object} [params] - Params to querystring
         * @param {Object} [options] - Options 
         * @return {Promise} - The result of $http
         */
        request (method, path, data = {}, params = {}, options = {}) {

            if (['GET', 'POST', 'PUT', 'DELETE'].indexOf(method) === -1) {
                return $q.reject(new Error("Invalid method"));
            }

            console.log(`api -> [${method}] ${path}`);

            var req = _.extend({
                method: method,
                url: `${API_URL}/${path}`,
                headers: {
                    "Content-Type": 'application/json',
                    "Accept": 'application/json'
                },
                data: data,
                params: params 
           
            }, options);

            return $http(req);

        }

        /**
         * Get path 
         * @param {String} path - The path 
         * @param {Object} [paran] - Params to querystring
         * @return {Promise}
         * @example
         *      ApiV1.get("users", { max: 20 })
         *          .then((users) => {
         *              // users.data <- the data 
         *          });
         */
        get (path, params) {
            return this.request('GET', path, {}, params);
        }

        /**
         * Post path 
         * @param {String} path - The path 
         * @param {Object} data - Data to send
         * @param {Object} [paran] - Params to querystring
         * @return {Promise}
         * @example
         *      ApiV1.post("users", { name: "Jhon", lastName: "Travolta" })
         *          .then((res) => {
         *              // res.status === 201
         *          });
         */
        post (path, data, params = {}, options = {}) {
            return this.request('POST', path, data, params, options);
        }

        /**
         * Put path 
         * @param {String} path - The path 
         * @param {Object} data - Data to send
         * @param {Object} [paran] - Params to querystring
         * @return {Promise}
         * @example
         *      ApiV1.post("users/32", { password: "123" })
         *          .then((res) => {
         *              // res.status === 200
         *          });
         */
        put (path, data, params = {}) {
            return this.request('PUT', path, data, params);
        }

        /**
         * delete path 
         * @param {String} path - The path 
         * @param {Object} [paran] - Params to querystring
         * @return {Promise}
         * @example
         *      ApiV1.delete("users/32", { force: true });
         */
        delete (path, params = {}) {
            return this.request('DELETE', path, {}, params);
        }

        /**
         * Get instance 
         */
        static getInstance() {
            if (!instance) {
                instance = new ApiV1();
            }

            return instance;

        }

        /**
         * Normalize data to underscore style
         * @param {Object} data 
         * @return {Object} 
         * @example
         *      Apiv1.normalize({lastName: 'Jhon'});
         *      // {last_name: 'Jhon'}
         */
        static normalize(data) {
            var newObj = {};

            if (_.isArray(data)) {
                return _.map(data, (item) => {
                    return ApiV1.normalize(item);
                });
            }

            if (!_.isObject(data)) {
                return data;
            }

            _.each(_.keys(data), (key) => {

                if (_.isObject(data[key]) && !_.isArray(data[key])) {
                    newObj[toUndorescore(key)] = ApiV1.normalize(data[key]);
                } else {
                    newObj[toUndorescore(key)] = data[key];
                }

            });

            return newObj;

        }

    }

    return ApiV1;

}];
