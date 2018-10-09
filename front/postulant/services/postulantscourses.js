"use strict";

/**
 * Postulant panel, postulations
 * @memberof Postulants
 * @ngdoc service
 * @name PostulantCoursesService
 */

const factory = function (CollectionService) {

    const getCollection = function () {
        const path = "postulant/panel/courses";
        return new CollectionService.Collection(path);
    };

    return {
        getCollection,
    };

};

module.exports = [
    "CollectionService",
    factory
];
