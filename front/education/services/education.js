"use strict";

/**
 * Education service
 * @memberof Education
 * @ngdoc service
 * @name EducationService
 */

const factory = function ($q, ApiService) {

    const _get = function(subpath, params = {}) {
        var path = `education/${subpath}`;
        return ApiService.getInstance().get(path, params) 
            .then((response) => {
                if (response.data) {
                    return response.data; 
                } else {
                    throw new Error("Invalid respose");
                }
            });
    };

    /**
     * Search institutions by name
     * @memberof EducationService
     * @param {string} s - Keyword to search
     * @return {Promise}
     */
    const searchInstitution = function (s) {
        if (s.length < 3) {
            return $q.resolve([]);
        }

        return _get('institution/search',{s});

    };

    /**
     * Get availables education grades
     * @memberof EducationService
     * @return {Promise}
     */

    const getGrades = function () {
        return _get('grades');
    };

    /**
     * Get availables languages
     * @memberof EducationService
     * @return {Promise}
     */

    const getLanguages = function () {
        return _get('languages');
    };

    return {
        searchInstitution,
        getGrades,
        getLanguages
    };

};

module.exports = [
    "$q",
    "Apiv1Service",
    factory
];
