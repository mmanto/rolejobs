"use strict";

module.exports = [
    "$q",
    "$rootScope",
    "$cookies",
/**
 * @ngdoc service 
 * @memberof accounts 
 * @name AuthService
 * @param {service} $q 
 * @param {service} $rootScope
 * @param {service} $cookies
 * @description 
 *      Auth provider service
 */
function ($q, $rootScope, $cookies) {

    var token =  $cookies.get("auth.token") || null;

    /**
     * Define the authorization token and emit 
     * @param {String} token - The token returned by API
     * @event {broadcast} auth.authorized - When authorized
     */
    const auth = function (_token) {
        token = _token;
        $cookies.put("auth.token", _token, {
            // @TODO Enabled in production
            // secure: true
        });
        $rootScope.$broadcast("auth.authorized");
    };

    return {
        auth
    };

}];
