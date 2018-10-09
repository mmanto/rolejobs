"use strict";

/**
 * Languages service
 * @memberof Education
 * @ngdoc service
 * @name LanguagesService
 */

const factory = function ($q, ApiService) {

    const list = function() {
        var path = `education/languages`;
        return ApiService.getInstance().get(path) 
            .then((response) => {
                if (response.data) {
                    return response.data; 
                } else {
                    throw new Error("Invalid respose");
                }
            });

    };

    return {
        list
    };

};

module.exports = [
    "$q",
    "Apiv1Service",
    factory
];
