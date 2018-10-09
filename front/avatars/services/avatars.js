"use strict";

/**
 * Avatars service
 * @memberof Avatars
 * @ngdoc service
 * @name AvatarsService
 */

const factory = function ($q, $rootScope, ApiService) {

    const chan = $rootScope.$new(true);
   
    const post = (subpath, data, params = {}, options = {}) => { 

        var path = `avatars/${subpath}`;

        return ApiService.getInstance().post(
            path,
            data,
            params,
            options)
            .then((res) => {
                return res.data;
            });
    };

    const uploadProfile = function (label, data) {

        if (typeof data === "undefined") {
            data = label;
            label = "default";
        }

        return post(
            `profile/${label}`,
            data,
            {},
            {
                headers: {
                    "Content-Type": 'text/plain',
                    "Accept": 'application/json'
                }
            })
            .then(() => {
                chan.$emit("change_profile_avatar");
            });
    };

    const on = function (eventName, listener) {
        return chan.$on(eventName, listener);
    };

    return {
        uploadProfile,
        on
    };

};

module.exports = [
    '$q',
    '$rootScope',
    'Apiv1Service', 
    factory
];
